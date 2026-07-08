input = getDirectory("Select Input Folder");
output = getDirectory("Select Output Folder");

processFolder(input);

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			processFolder(input + File.separator + list[i]);
		if(endsWith(list[i], ".tif"))
			processFile(input, output, list[i]);
	}
}


function processFile(input, output, file) {
	open(input + File.separator + file);
	print("Processing: " + input + File.separator + file);
	selectWindow(file);
	run("8-bit");
    run("Subtract Background...", "rolling=10  sliding disable" + "stack");
    setAutoThreshold("Otsu");
    //run("Threshold...");
    setThreshold(10, 255, "raw");
    //setThreshold(10, 255);
	run("Convert to Mask", "method=Otsu background=Light convert");
	run("Set Scale...", "distance=254 known=1 unit=mm");
	run('TrackMate',
    "use_gui=false " +
    "save_to=[" + output + File.separator + file + "] " +
    "export_to=[" + output + File.separator + file + "] " +
    "display_results=true " +
    "radius=0.5 " +
    "threshold=2 " +
    "subpixel=false " +
    "median=false " +
    "channel=1 " +
    "max_distance=5 " +
    "max_gap_distance=0 " +
    "max_frame_gap=0"
    );
	print("Saving to: " + output);
	saveAs("Tiff", output + File.separator +  file);
		
}

run("Close All");




