// Generate whole class tree

(
// recursive function to get class names

~func = { arg classname, idx, file;
	var subclasses = classname.subclasses;

	if (subclasses != nil, {file.write(":\n"); }, {file.write("\n");});

	subclasses.do({ arg class;
		var pre = "";

		idx.do({ pre = pre ++ " "});

		//(pre ++ class.name ++ "\n").postln;
		if (subclasses.size == 1,
			{ file.write(pre + " " + class.name) },
			{ file.write(pre + "-" + class.name) });

		~func.(class, idx+2, file);
	})
}
)



(
// file creation

var f = File.open(Document.current.dir ++ "/tree.yaml".standardizePath, "w");
f.write("Object");
~func.(Object, 1, f);
f.close
)




(

// create yaml file with classnames and methods

var f = File.open(Document.current.dir ++ "/classes_with_methods.yaml".standardizePath, "w");
var c = File.use(Document.current.dir ++ "/only_classes.txt".standardizePath,
	"r",
	{ |f| f.readAllString });

d = c.split($\n);

d.do({ arg i;
	var to_compile = (i++".methods").compile;
	f.write(i++":\n");
	to_compile.value.do({ arg method; f.write((" - \"" ++ method.name ++ "\"\n")) });
});
f.close

)









