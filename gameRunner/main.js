var testFile = "tests.csv"
var lambdamansPath = "Lambdamans/"
var mapsPath = "Maps/"
var ghostsPath = "Ghosts/"

var fs = require('fs');
var vm = require('vm');

// Load game files
vm.runInThisContext(fs.readFileSync('game.html.js'))
vm.runInThisContext(fs.readFileSync('game.js'))

// Read test file
var tests = fs.readFileSync(testFile).toString().trim().split("\n");
for (i in tests) {
    console.log("Test" + (parseInt(i) + 1) + ": " + tests[i]);

    var inputs = tests[i].split(",");
    if (inputs.length == 3) {
        lambdaman = fs.readFileSync(lambdamansPath + inputs[0].trim()).toString().replace(/\r/g, "").trim();
        map = fs.readFileSync(mapsPath + inputs[1].trim()).toString().replace(/\r/g, "").trim();
        var ghostFiles = inputs[2].trim().split("|");
        ghosts = ghostFiles.map(function (file) { return fs.readFileSync(ghostsPath + file).toString().replace(/\r/g, "").trim() });
        //console.log(lambdaman);
        //console.log(map);
        //console.log(ghosts);

        //console.log("Run started at: " + new Date())
        try {
            load();
            run();
        } catch (e) {
            console.log("Error occurred: " + e)
        }
		//console.log("Run completed at: " + new Date())
    }
    else {
        console.log("Invalid number of input files. Skipping this test.")
    }
    console.log();
}