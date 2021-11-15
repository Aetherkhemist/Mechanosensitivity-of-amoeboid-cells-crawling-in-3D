///This macro takes a stack of the images acquired over a specific Z-slice over time, 
///projects it as a sum of all the time points and creates a binary image (a mask) for that stack over time. 
///This mask will serve to analyse only the area surrounding the cell instead of the all image!


print("\\Clear");
dir= getDirectory("Choose file folder");
print("Dir:"+dir);

list = getFileList(dir);
//setBatchMode(true);
for( i=0; i<list.length;i++){
	if(endsWith(list[i],".tif") ==true) { 
		path=dir+list[i];
		print(path);
		run("Bio-Formats Importer", "open=["+path+"] color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
		save_name=File.nameWithoutExtension();
		title=getTitle();
		print("Title:" + title);

		selectWindow(title);
		
		run("Brightness/Contrast...");
		resetMinAndMax();
		run("Duplicate...", "title=duplicate duplicate ");
		selectWindow("duplicate");
		run("Subtract Background...", "rolling=50 stack");
		run("Z Project...", "projection=[Sum Slices]");
		run("Subtract Background...", "rolling=12 create");
		run("8-bit");
		run("Auto Threshold", "method=Triangle white");
		run("Analyze Particles...", "  show=Masks display exclude clear summarize");
		run("Maximum...");
		///50
		run("Median...");
		///5
		run("Convert to Mask");
		
		run("Analyze Particles...", "  show=Masks display exclude clear summarize");
		
		save_dir= getDirectory("Choose file folder");
		selectWindow("Mask of Mask of SUM_duplicate");
		
		saveAs("Tiff",save_dir+File.separator+save_name+"_mask.tif");
		close('*');
		}
}

