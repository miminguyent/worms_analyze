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
	run("Subtract Background...", "rolling=10  sliding disable");
	setAutoThreshold("Otsu");
	//run("Threshold...");
	setThreshold(10, 255, "raw");
	//setThreshold(10, 255);
	run("Convert to Mask");
	print("Saving to: " + output);
	saveAs("Tiff", output + File.separator +  file);
		
}

run("Close All");




