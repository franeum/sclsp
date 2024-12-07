

(
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
var f = File.open(Document.current.dir ++ "/tree.yaml".standardizePath, "w");
f.write("Object");
~func.(Object, 1, f);
f.close
)


