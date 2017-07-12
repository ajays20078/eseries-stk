SET var=%CD%
SET driveSuffix=%var::\=/%

SET fixSlashes=%driveSuffix:\=/%

SET unixPath=/%fixSlashes%/ansiblelink

docker run -v %unixPath%:/root/ansiblelink -ti myansiblessh
PAUSE