publish: release-sink
	mkdir -p src/sink
	cp -a sink/target/oss-sink-window-connector-1.0-SNAPSHOT.jar src/sink/oss-sink-window-connector-1.0-SNAPSHOT.jar
	s cli registry publish
	rm -rf src/sink
release-sink:
	cd sink && mvn clean package
