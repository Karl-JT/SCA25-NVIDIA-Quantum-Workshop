# Simple Makefile

OUTPUTFILEBASE=libprofile_util
CXXFLAGS = -fPIC -std=c++17 -O2
OMPFLAGS ?= -fopenmp
EXTRAFLAGS ?= 
COMPILER ?=$(CXX)
COMPILERFLAGS = $(CXXFLAGS) $(EXTRAFLAGS)

BUILDTYPE ?= serial
DEVICETYPE= cpu  
BUILDNAME ?=

OBJS = obj/git_revision.o obj/mem_util.o obj/time_util.o obj/thread_affinity_util.o obj/profile_util.o
LIB = lib/$(OUTPUTFILEBASE)$(BUILDNAME)

GIT_COMMIT := $(shell git rev-parse HEAD)
GIT_IS_DIRTY := $(shell git diff HEAD | wc -l)

$(LIB).so: $(OBJS)
	@echo "Making $(BUILDTYPE) for $(DEVICETYPE) library"
	$(CXX) -shared $(OBJS) -o $(LIB).so
	rm $(OBJS)

obj/git_revision.o: src/git_revision.cpp.in
	@cp src/git_revision.cpp.in src/git_revision.cpp 
	@if [ ${GIT_IS_DIRTY} == 0 ]; then\
		sed -i "s:\@GIT_HAS_LOCAL_CHANGES\@::g" src/git_revision.cpp;\
	else\
		sed -i "s:\@GIT_HAS_LOCAL_CHANGES\@:DIRTY:g" src/git_revision.cpp;\
	fi
	@sed -i "s:\@GIT_SHA1\@:${GIT_COMMIT}:g" src/git_revision.cpp
	$(COMPILER) $(COMPILERFLAGS) -Iinclude/ -c src/git_revision.cpp -o obj/git_revision.o
	@rm src/git_revision.cpp

#$(OBJS): obj/%.o : src/%.cpp include/profile_util.h

obj/%.o: src/%.cpp include/profile_util.h
	$(COMPILER) $(COMPILERFLAGS) -Iinclude/ -c $< -o $@


clean:
	rm -f $(LIB).so
