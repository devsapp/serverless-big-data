publish: release-transform
	mkdir -p src/transform
	cp -a transform/target/oss-file-format-transformer-1.0-SNAPSHOT.jar src/transform/oss-file-format-transformer-1.0-SNAPSHOT.jar
	s cli registry publish
	rm -rf src/transform
release-transform:
	cd transform && mvn clean package
