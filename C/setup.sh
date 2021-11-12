apt-get -y install autoconf libtool

cd /autograder

#CJ: Grab cpputest from my fork (so that updates don't break stuff) and build it from source so that we can make use of MakefileWorker.mk
git clone https://github.com/cgjeffries/cpputest.git
cd cpputest
autoreconf . -i
./configure
make

chmod +x /autograder/source/run_cpputest.sh

dos2unix /autograder/source/run_cpputest.sh