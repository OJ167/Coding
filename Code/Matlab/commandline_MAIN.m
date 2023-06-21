
clc; clear

%% Settings

nRuns=2;                                                                               % Number of runs to analyse
directories = {uigetdir,};%, uigetdir};%, uigetdir, uigetdir, uigetdir};%,uigetdir,uigetdir};                      % Comment out how many are not needed
pairwisePre = {0,0,0,0,0,0,0,0,0,0}; % 0 for [A+B], [B+C], [C+D]... sequencing style, and 1 for [A+B], [C+D], [E+F]... sequencing style
bgSubPre = {1,1,1,1,1,1,1,1,1};                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             % 1 Subtracts bg, 0 skips this step

% LOOOOOOP
for aa = 1:nRuns
    tic
    directory = char(directories{aa});
    disp(directory)
    nr_of_cores = 1; % integer, 1 means single core, greater than 1 means parallel (42 on big machine)
    pairwise = pairwisePre{aa};
    bgSub = bgSubPre{aa};
    
    if nr_of_cores > 1
        try
            local_cluster=parcluster('local'); % single node
            corenum =  local_cluster.NumWorkers ; % fix : get the number of cores available
        catch
            warning('on');
            warning('parallel local cluster can not be created, assigning number of cores to 1');
            nr_of_cores = 1;
        end
    end
    %% Create list of images inside user specified directory
    suffix='*.tiff'; %*.bmp or  or *.jpg or .tiff or *.jpeg
    direc = dir([directory,filesep,suffix]);
    filenames={};
    [filenames{1:length(direc),1}] = deal(direc.name);
    amount = length(filenames);
    
    [fileZeroPath, fileZeroName, fileZeroExt] = fileparts(fullfile(directory, filenames{1}));
    if fileZeroName(end-1:end) == '-0'
        disp('Unsorted')
        for i=1:1:amount
            [path, name, ext] = fileparts(fullfile(directory, filenames{i}));
            locateNumber = strfind(name,'-');
            number = num2str(str2num(name(locateNumber(2)+1:end)),'%06.f');
            nameNew = [number '-' name(1:locateNumber(2)-1)];
            movefile([path '\' name ext],[path '\' nameNew ext])
        end
        disp('Sorted')
    else
        disp('Sorted')
    end
    
    direc = dir([directory,filesep,suffix]);
    filenames={};
    [filenames{1:length(direc),1}] = deal(direc.name);
    filenames = sortrows(filenames); %sort all image files
    
    generate_BG_img(bgSub,pairwise,directory,filenames,amount)
    
    %% Standard PIV Settings
    s = cell(13,2); % To make it more readable, let's create a "settings table"
    %Parameter                          %Setting           %Options
    s{1,1}= 'Int. area 1';              s{1,2}=64;         % window size of first pass
    s{2,1}= 'Step size 1';              s{2,2}=32;         % step of first pass
    s{3,1}= 'Subpix. finder';           s{3,2}=1;          % 1 = 3point Gauss, 2 = 2D Gauss
    s{4,1}= 'Mask';                     s{4,2}=[];         % If needed, generate via: imagesc(image); [temp,Mask{1,1},Mask{1,2}]=roipoly;
    s{5,1}= 'ROI';                      s{5,2}=[];         % Region of interest: [x,y,width,height] in pixels, may be left empty
    s{6,1}= 'Nr. of passes';            s{6,2}=3;          % 1-4 nr. of passes
    s{7,1}= 'Int. area 2';              s{7,2}=32;         % second pass window size
    s{8,1}= 'Int. area 3';              s{8,2}=16;         % third pass window size
    s{9,1}= 'Int. area 4';              s{9,2}=16;         % fourth pass window size
    s{10,1}='Window deformation';       s{10,2}='*linear'; % '*spline' is more accurate, but slower
    s{11,1}='Repeated Correlation';     s{11,2}=0;         % 0 or 1 : Repeat the correlation four times and multiply the correlation matrices.
    s{12,1}='Disable Autocorrelation';  s{12,2}=0;         % 0 or 1 : Disable Autocorrelation in the first pass.
    s{13,1}='Correlation style';        s{13,2}=0;         % 0 or 1 : Use circular correlation (0) or linear correlation (1).
    
    %% Standard image preprocessing settings
    p = cell(10,1);
    %Parameter                       %Setting           %Options
    p{1,1}= 'ROI';                   p{1,2}=s{5,2};     % same as in PIV settings
    p{2,1}= 'CLAHE';                 p{2,2}=1;          % 1 = enable CLAHE (contrast enhancement), 0 = disable
    p{3,1}= 'CLAHE size';            p{3,2}=50;         % CLAHE window size
    p{4,1}= 'Highpass';              p{4,2}=0;          % 1 = enable highpass, 0 = disable
    p{5,1}= 'Highpass size';         p{5,2}=15;         % highpass size
    p{6,1}= 'Clipping';              p{6,2}=0;          % 1 = enable clipping, 0 = disable
    p{7,1}= 'Wiener';                p{7,2}=0;          % 1 = enable Wiener2 adaptive denoise filter, 0 = disable
    p{8,1}= 'Wiener size';           p{8,2}=3;          % Wiener2 window size
    p{9,1}= 'Minimum intensity';     p{9,2}=0.0;        % Minimum intensity of input image (0 = no change)
    p{10,1}='Maximum intensity';     p{10,2}=1.0;       % Maximum intensity on input image (1 = no change)
    
    %% PIV analysis loop
    if pairwise == 1
        if mod(amount,2) == 1 %Uneven number of images?
            disp('Image folder should contain an even number of images.')
            %remove last image from list
            amount=amount-1;
            filenames(size(filenames,1))=[];
        end
        
        disp(['Found ' num2str(amount) ' images (' num2str(amount/2) ' image pairs).'])
        x=cell(amount/2,1);
        y=x;
        u=x;
        v=x;
    else
        disp(['Found ' num2str(amount) ' images'])
        x=cell(amount-1,1);
        y=x;
        u=x;
        v=x;
    end
    
    typevector=x; %typevector will be 1 for regular vectors, 0 for masked areas
    correlation_map=x; % correlation coefficient
    
    %% Pre-load the image names out side of the parallelizable loop
    slicedfilename1=cell(0);
    slicedfilename2=cell(0);
    j = 1;
    for i=1:1+pairwise:amount-1
        slicedfilename1{j}=filenames{i}; % begin
        slicedfilename2{j}=filenames{i+1}; % end
        j = j+1;
    end
    
    
    %% Main PIV analysis loop:
    % parallel
    if nr_of_cores > 1
        
        if pivparpool('size')<nr_of_cores
            pivparpool('open',nr_of_cores);
        end
        
        parfor i=1:size(slicedfilename1,2)  % index must increment by 1
            
            [x{i}, y{i}, u{i}, v{i}, typevector{i},correlation_map{i}] = ...
                piv_analysis_MAIN(directory, slicedfilename1{i}, slicedfilename2{i},p,s,nr_of_cores,false);
        end
    else % sequential loop
        
        for i=1:size(slicedfilename1,2)  % index must increment by 1
            
            [x{i}, y{i}, u{i}, v{i}, typevector{i},correlation_map{i}] = ...
                piv_analysis_MAIN(directory, slicedfilename1{i}, slicedfilename2{i},p,s,nr_of_cores,true);
            
            disp([int2str((i+1)/amount*100) ' %']);
            
        end
    end
    
    
    %% PIV postprocessing loop
    % Standard image post processing settings
    
    r = cell(6,1);
    %Parameter     %Setting                                     %Options
    r{1,1}= 'Calibration factor, 1 for uncalibrated data';      r{1,2}=1;                   % Calibration factor for u
    r{2,1}= 'Calibration factor, 1 for uncalibrated data';      r{2,2}=1;                   % Calibration factor for v
    r{3,1}= 'Valid velocities [u_min; u_max; v_min; v_max]';    r{3,2}=[-50; 50; -50; 50];  % Maximum allowed velocities, for uncalibrated data: maximum displacement in pixels
    r{4,1}= 'Stdev check?';                                     r{4,2}=1;                   % 1 = enable global standard deviation test
    r{5,1}= 'Stdev threshold';                                  r{5,2}=7;                   % Threshold for the stdev test
    r{6,1}= 'Local median check?';                              r{6,2}=1;                   % 1 = enable local median test
    r{7,1}= 'Local median threshold';                           r{7,2}=3;                   % Threshold for the local median test
    
    u_filtered=cell(size(u));
    v_filtered=cell(size(v));
    typevector_filt=typevector;
    
    if nr_of_cores >1 % parallel
        
        
        if pivparpool('size')<nr_of_cores
            pivparpool('open',nr_of_cores);
        end
        
        
        parfor PIVresult=1:size(x,1)
            
            [u_filtered{PIVresult,1}, v_filtered{PIVresult,1},typevector_filt{PIVresult,1}]= ...
                post_proc_wrapper(u{PIVresult,1},v{PIVresult,1},typevector{PIVresult,1},r,true);
            
        end
        
    else % sequential loop
        
        for PIVresult=1:size(x,1)
            
            [u_filtered{PIVresult,1}, v_filtered{PIVresult,1},typevector_filt{PIVresult,1}]= ...
                post_proc_wrapper(u{PIVresult,1},v{PIVresult,1},typevector{PIVresult,1},r,true);
            
        end
        
    end
    
    %% clean up parallel pool, and cluster
    
    if nr_of_cores >1 % parallel
        poolobj = gcp('nocreate'); % GET the current parallel pool
        if ~isempty(poolobj ); delete(poolobj );end
        clear local_cluster;
    end
    
    %%
    c = clock;
    disp(['DONE.          Time = ' int2str(c(4)) ':' int2str(c(5))])
    
    lastSlashPosition = find(directory == '\', 1, 'last');
    parentFolder = directory(1:lastSlashPosition-1);
    
    saveDirectory1 = fullfile(parentFolder,'data', 'PIV_export.mat');
    save(saveDirectory1,'u_filtered','v_filtered', '-v7.3');
    saveDirectory2 = fullfile(parentFolder,'data', 'PIV_export_unfiltered.mat');
    save(saveDirectory2,'u','v', '-v7.3');
    timer = toc;
    if pairwise == 0  
        averagetime = timer/amount;
        disp(['Time per image:  ' num2str(averagetime) 's'])
    else
        averagetime = timer/(0.5 * amount);
        disp(['Time per image:  ' num2str(averagetime) 's'])
    end
    clearvars -except p s r x y u v typevector directory directories nRuns pairwise pairwisePre bgSubPre filenames u_filtered v_filtered typevector_filt correlation_map bgSub
    
end


function generate_BG_img(bgSub,pairwise,directory,filenames,amount)
if bgSub==1
    if not(isfolder(fullfile(directory,'bgImage')))     % folder does not exist already
        disp('BG not present, calculating now')
        % Calculate BG for all images....
        % read first image to determine properties
        [~,~,ext] = fileparts(fullfile(directory, filenames{1}));
        if strcmp(ext,'.b16')
            image1=f_readB16(fullfile(directory, filenames{1}));
            image2=f_readB16(fullfile(directory, filenames{2}));
            imagesource='b16_image';
        else
            image1=imread(fullfile(directory, filenames{1}));
            image2=imread(fullfile(directory, filenames{2}));
            imagesource='normal_pixel_image';
        end
        
        classimage=class(image1); %memorize the original image format (double, uint8 etc)
        
        if size(image1,3)>1
            image1=rgb2gray(image1); %rgb2gray conserves the variable class (single, double, uint8, uint16)
            image2=rgb2gray(image2);
            colorimg=1;
        else
            colorimg=0;
        end
        counter=1;
        
        %convert all image types to double, ranging from 0...1
        if strcmp(classimage,'double')==1 %double stays double
            %do nothing
        elseif strcmp(classimage,'single')==1 %e.g. 32bit tif, ranges from 0...1
            image1=double(image1);
            image2=double(image2);
        elseif strcmp(classimage,'uint16')==1 %e.g. 16bit tif, ranges from 0...65535
            image1=double(image1)/65535;
            image2=double(image2)/65535;
        elseif strcmp(classimage,'uint8')==1 %0...255
            image1=double(image1)/255;
            image2=double(image2)/255;
        end
        
        if pairwise==0 %time-resolved
            start_bg=2;
            skip_bg=1;
        else
            start_bg=3;
            skip_bg=2;
        end
        
        
        
        %perform image addition
        %if timeresolved: generate only one background image from all
        %images
        %if not: generate two background images. One from even frames,
        %one from odd frames
        updatecntr=0;
        for i=start_bg:skip_bg:amount
            counter=counter+1;
            updatecntr=updatecntr+1;
            if strcmp('b16_image',imagesource)
                image_to_add1 = f_readB16(fullfile(directory, filenames{i})); %will be double
                if pairwise==1 %not time-resolved
                    image_to_add2 = f_readB16(fullfile(directory, filenames{i+1}));
                end
            elseif strcmp('normal_pixel_image',imagesource)
                image_to_add1 = imread(fullfile(directory, filenames{i}));
                if pairwise==1 %not time-resolved
                    image_to_add2 = imread(fullfile(directory, filenames{i+1})); %will be double or uint8
                end
            elseif strcmp('from_video',imagesource)
                image_to_add1 = read(video_reader_object,video_frame_selection(i));
                if pairwise==1 %not time-resolved
                    image_to_add2 = read(video_reader_object,video_frame_selection(i+1));
                end
            end
            %images arrive in their original format here
            %convert everything to grayscale and double [0...1]
            if colorimg==1
                image_to_add1 = rgb2gray(image_to_add1); %will conserve image class
                if pairwise==1 %not time-resolved
                    image_to_add2 = rgb2gray(image_to_add2);
                end
            end
            if strcmp(classimage,'double')==1
                image_to_add1=image_to_add1;
                if pairwise==1 %not time-resolved
                    image_to_add2=image_to_add2;
                end
            end
            if strcmp(classimage,'single')==1
                image_to_add1=double(image_to_add1);
                if pairwise==1 %not time-resolved
                    image_to_add2=double(image_to_add2);
                end
            end
            if strcmp(classimage,'uint8')==1
                image_to_add1=double(image_to_add1)/255;
                if pairwise==1 %not time-resolved
                    image_to_add2=double(image_to_add2)/255;
                end
            end
            if strcmp(classimage,'uint16')==1
                image_to_add1=double(image_to_add1)/65535;
                if pairwise==1 %not time-resolved
                    image_to_add2=double(image_to_add2)/65535;
                end
            end
            %now everything is double [0...1]
            %Sum up  all images
            image1=image1 +image_to_add1;
            if pairwise==1 %not time-resolved
                image2=image2+image_to_add2;
            end
        end %of for loop and image summing
        
        %divide the sum by the amount of summed images
        image1_bg=image1/counter;
        if pairwise==1 %not time-resolved
            image2_bg=image2/counter;
        end
        
        %Convert back to original image class, if not double anyway
        if strcmp(classimage,'uint8')==1 %#ok<*STISA>
            image1_bg=uint8(image1_bg*255);
            if pairwise==1 %not time-resolved
                image2_bg=uint8(image2_bg*255);
            end
        end
        
        if strcmp(classimage,'single')==1
            image1_bg=single(image1_bg);
            if pairwise==1 %not time-resolved
                image2_bg=single(image2_bg);
            end
        end
        
        if strcmp(classimage,'uint16')==1
            image1_bg=uint16(image1_bg*65535);
            if pairwise==1 %not time-resolved
                image2_bg=uint16(image2_bg*65535);
            end
        end
        
        
        
        
        
        mkdir(directory, 'bgImage');
        imwrite(image1_bg,fullfile(directory,'bgImage','image1_bg.tiff'));
        
        if pairwise==1 %not time-resolved
            imwrite(image2_bg,fullfile(directory,'bgImage','image2_bg.tiff'));
        else
            imwrite(image1_bg,fullfile(directory,'bgImage','image2_bg.tiff'))
        end
        
    else
        disp('BG exists')
    end
end
end


function [u_filtered, v_filtered, typevector_filt] = post_proc_wrapper(u,v,typevector,post_proc_setting,paint_nan)
% wrapper function for PIVlab_postproc

% INPUT
% u, v: u and v components of vector fields
% typevector: type vector
% post_proc_setting: post processing setting
% paint_nan: bool, whether to interpolate missing data

% OUTPUT
% u_filt, v_filt: post-processed u and v components of vector fields
% typevector_filt: post-processed type vector


[u_filtered,v_filtered] = PIVlab_postproc(u,v, ...
    post_proc_setting{1,2},...
    post_proc_setting{2,2},...
    post_proc_setting{3,2},...
    post_proc_setting{4,2},...
    post_proc_setting{5,2},...
    post_proc_setting{6,2},...
    post_proc_setting{7,2});

typevector_filt = typevector; % initiate
typevector_filt(isnan(u_filtered))=2;
typevector_filt(isnan(v_filtered))=2;
typevector_filt(typevector==0)=0; %restores typevector for mask

if paint_nan
    u_filtered=inpaint_nans(u_filtered,4);
    v_filtered=inpaint_nans(v_filtered,4);
end


end