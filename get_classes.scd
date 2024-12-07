


(
var file = File.open("~/Documenti/sclsp/classes.txt".standardizePath, "w");

Object.allSubclasses.do({ arg name;
	file.write(name.asString++"\n");
});

file.close;
)



(
var file = File.open("~/Documenti/sclsp/classes.txt".standardizePath, "w");

Object.allSubclasses.do({ arg name;
	file.write(name.asString++"\n");
	name.methods.do({
		arg method;
		//method.name.postln;
		file.write("\t"++method.name.asString++"\n");
	});
});

file.close;
)

Array.dumpMethodList.do({|i| i.postln})

Array.allMethodsDo()
Array.makeMethodList

