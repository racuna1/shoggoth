apt-get -y install openjdk-11-jdk python3-pip

# The following lines are to make sure we can install packages from maven
# See https://bugs.launchpad.net/ubuntu/+source/ca-certificates-java/+bug/1396760
# and https://github.com/docker-library/openjdk/issues/19#issuecomment-70546872
apt-get install --reinstall ca-certificates-java
update-ca-certificates -f

#RA: manually fetch maven 3.8.3 instead of using default 3.6.0 package
cd /autograder
wget https://mirror.olnevhost.net/pub/apache/maven/maven-3/3.8.3/binaries/apache-maven-3.8.3-bin.tar.gz
tar xzvf apache-maven-3.8.3-bin.tar.gz

#RA: install jh61b manually
cd /autograder/source
export PATH="/autograder/apache-maven-3.8.3/bin:$PATH"
mvn install:install-file -Dfile=lib/jh61b-1.0.jar

# cache maven packages and plugins during Dock build
mvn dependency:go-offline

# install packages for shoggoth
pip3 install -r requirements.txt


#CJ: C requirements (maybe turn these off contitionally?)

apt-get -y install autoconf libtool

cd /autograder

#CJ: Grab cpputest from my fork (so that updates don't break stuff) and build it from source so that we can make use of MakefileWorker.mk
git clone https://github.com/cgjeffries/cpputest.git
cd cpputest
autoreconf . -i
./configure
make

# grabs pycparser
cd /autograder
git clone https://github.com/eliben/pycparser.git
cd pycparser
python3 setup.py install

chmod +x /autograder/source/run_cpputest.sh

dos2unix /autograder/source/run_cpputest.sh