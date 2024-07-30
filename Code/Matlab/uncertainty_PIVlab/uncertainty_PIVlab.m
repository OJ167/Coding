clc
close all
clear

%load the intermediate result from PIVfft_multi. It contains all information that was generated during the cross-correlation window deformation.
load analysis_data.mat
%We need to use this data to perform the uncertainty calculation.
%The idea is from this paper: https://github.com/Shrediquette/PIVlab/files/6736049/PIV_uncertainty_sciacchitano2013.pdf
%Their code is available here:
%http://piv.de/uncertainty/UncertaintyCodes/ParticleDisparity_Code.zip
%But I always find it easier to code my own stuff. It is more fun too.

%What they do is the following:
%After image deformation: multiply images, then threshold. White pixels represent particles tht are present in A and B. 
%Use subpixel estimator to find displacement of each particle in A and B. 
%The "mismatch" is then a measure for the uncertainty (after some statistical stuff that I still have to look at).

%% Uncertainty calculation
example_index = 201; %figures are plotted with "interrogation area number X" to show some emeplary figures.

%image1_cut are all interrogation areas from image A
%image2_cut are all interrogation areas from image B (deformed, ideally they should then look like image1_cut)
%if you want to have a look: 
imagesc(image1_cut(:,:,example_index));colormap('gray');title('Interrogation area A');figure;imagesc(image2_cut(:,:,example_index));colormap('gray');title('Interrogation area B (deformed)')

%lowpass filter
image1_cut = imfilter(image1_cut,fspecial('gaussian',[3 3]));
image2_cut = imfilter(image2_cut,fspecial('gaussian',[3 3]));

%This should now give high values where particles are present at the same position in both images:
multiplied_images = image1_cut(:,:,:) .* image1_cut(:,:,:);
figure;imagesc(multiplied_images(:,:,example_index));colormap('gray');title('Multiplied interrogation areas')

max_val=max(multiplied_images,[],[1 2]); %maximum for each slice

%Binarize the result with a relatively strict threshold. Should result in a few pixels that highlight the position of matching particle pairs
multiplied_images_binary=imbinarize(multiplied_images./max_val,0.75);
figure;imagesc(multiplied_images_binary(:,:,example_index));colormap('gray');title('Binarized locations of matching particle pairs')
%Here I should find some metrics to select somethin like "the five most prominent particles", and discard all other "particles" (that probably aren't even particles

%multiplied_images_binary = bwareaopen(multiplied_images_binary, 2); %remove everything with less than n pixels, can be done to keep only large particle pairs
for islice=1:size(multiplied_images_binary,3)
	multiplied_images_binary(:,:,islice) = bwmorph(multiplied_images_binary(:,:,islice), 'shrink', inf);
end

figure;imagesc(multiplied_images_binary(:,:,example_index));colormap('gray');title('Binarized locations of matching particle pairs, reduced to single pixels')

%remove pixels at borders (otherwise subpixfinder will fail)
multiplied_images_binary(:,1,:)=0;multiplied_images_binary(:,end,:)=0;
multiplied_images_binary(1,:,:)=0;multiplied_images_binary(end,:,:)=0;
amount_of_particles_pairs_per_IA = squeeze(sum(multiplied_images_binary,[1 2]));

%find all coordinates of matchingparticle pairs
[y_img, x_img, z_img] = ind2sub(size(multiplied_images_binary), find(multiplied_images_binary==1));
%the above contains the integer locations of matching particle pairs. 
%Now I will use a subpix estimator to find the subpixel accurate position of the matching particles in interrogation area a and in interrogation area B.
%ideally, they should be identical of course if the windows deformation was perfect.

[peakx_A, peaky_A] = multispot_SUBPIXGAUSS(image1_cut, x_img, y_img, z_img); 
[peakx_B, peaky_B] = multispot_SUBPIXGAUSS(image2_cut, x_img, y_img, z_img);
%Actually, the above shouldn't give peak coordinates that differ more than 1 or 2 pixels..? I need to check this.

%{
From the paper:
Each point (i, j) where ? is non-null indicates a particle
image pair; the peak of the corresponding particle images is
detected in I1 and I2 in a ___neighborhood of search radius r___
(typically 1 or 2 pixels), centered in (i, j).
%}

xdisparity=peakx_A-peakx_B;
ydisparity=peaky_A-peaky_B;

figure;plot(xdisparity);title('The mismatch (in px) of matching particles in int area A & B\newlineI wonder why it is sometimes extremely high...?\NewlineThe mismatch is sometimes larger than the image size...?')

%The paper says that 'the search radius is limited to 1 or two pixels'. So I will discard everything 
%that has a difference larger than 1.5 pixels. Because then the particles did not match well, 
%and probably they aren't matchin particles but just some poorly matching noise or something?

%we identify particles that are visible at the same position in image A and B (ideally, after image deformation all particles should be in identical positions.
%If the disparity is larger than the particle radius, then this can't be real, because then these particles did not have an overlap initially and something must have gone wrong. But what...?

threshold=1.5;
xdisparity (xdisparity>threshold | xdisparity<-threshold)=nan;
ydisparity (ydisparity>threshold | ydisparity<-threshold)=nan;

%I am adding the mismatch in x and y direction:
total_disparity=(xdisparity+ydisparity)/2;

figure;histogram(total_disparity);title('This is the distribution of particle mismatches')

%Find the mean and stdev of the mismatch per interrogation area
per_slice_stdev=zeros(size(multiplied_images,3),1);
per_slice_mean=zeros(size(multiplied_images,3),1);
for slice_no=1:size(multiplied_images,3)
	%for every slice...
	idx=find(z_img==slice_no);
	per_slice_stdev(slice_no,1)=std(total_disparity(idx),'omitnan');
	per_slice_mean(slice_no,1)=mean(total_disparity(idx),'omitnan');
end

figure;histogram(per_slice_mean);title('Mean mismatch distribution over all interrogation areas (in px)')
figure;histogram(per_slice_stdev);title('Stdev of mismatch distribution over all interrogation areas (in px)')

%Equation 4 from the paper:
disp_error = sqrt(per_slice_mean.^2  + sqrt(per_slice_stdev ./ sqrt(amount_of_particles_pairs_per_IA)));
figure;histogram(disp_error);title('Estimation of the magnitude of the actual error (?)')


%Convert vector back to matrix
disp_error = permute(reshape(disp_error, [size(xtable')]), [2 1 3]);


figure;imagesc(disp_error);colorbar;title('Space-resolved error of the PIV data (in px)')

velocity_magnitude=(utable.^2+vtable.^2).^0.5;
figure;imagesc(disp_error./velocity_magnitude *100);colorbar;title('Space-resolved error of the PIV data (in PERCENT)\newlineSeems to be way too high. Something is wrong?')
caxis([0 100]);



function [peakx, peaky] = multispot_SUBPIXGAUSS(image_data, x, y, z)
%{
xi = find(~((x <= (size(image_data,2)-1)) & (y <= (size(image_data,1)-1)) & (x >= 2) & (y >= 2)));
x(xi) = [];
y(xi) = [];
z(xi) = [];
%}
xmax = size(image_data, 2);
if(numel(x)~=0)
	ip = sub2ind(size(image_data), y, x, z);
	f0 = log(image_data(ip));
	f1 = log(image_data(ip-1));
	f2 = log(image_data(ip+1));
	peaky = y + (f1-f2)./(2*f1-4*f0+2*f2);
	f0 = log(image_data(ip));
	f1 = log(image_data(ip-xmax));
	f2 = log(image_data(ip+xmax));
	peakx = x + (f1-f2)./(2*f1-4*f0+2*f2);
end
end
