##
## Bulid and load Metatab data packages
## for comments and course-enrollments
##


S3_BUCKET=library.metatab.org


PACK_DIR=_build

.PHONY: $(PACK_DIR) clean build s3 ckan list info
	
default: build ;
	
# List all of the targets
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs
	
	

PACKAGE_MARKERS = $(patsubst %,$(PACK_DIR)/%.build,$(PACKAGE_NAMES))
S3_MARKERS = $(patsubst %,$(PACK_DIR)/%.s3,$(PACKAGE_NAMES))
CKAN_MARKERS = $(patsubst %,$(PACK_DIR)/%.ckan,$(PACKAGE_NAMES))

$(PACK_DIR):
	mkdir -p $(PACK_DIR)


# Build a package file in the packages
# directory
$(PACK_DIR)/%.build :  %/metadata.csv
	@echo ======== BUILD $* from $* =======
	mkdir -p $(PACK_DIR)
	cd  $* && mp --exceptions build -f -z && \
	cd .. && touch $(PACK_DIR)/$*.build
	mp index $* 		
	
$(PACK_DIR)/%.s3: $(PACK_DIR)/%.build
	@echo ======== S3 $* \( $@ \) =======
	mp s3 -s $(S3_BUCKET) $*  && touch $(PACK_DIR)/$*.s3
	touch -r $(PACK_DIR)/$*.build $*/metadata.csv # mp s3 updates the metadata, but we don't want to re-trigger build
	
$(PACK_DIR)/%.ckan: $(PACK_DIR)/%.s3
	@echo ======== CKAN $* \( $@ \) =======
	mp ckan  $* && touch $(PACK_DIR)/$*.ckan 
	touch -r $(PACK_DIR)/$*.build $*/metadata.csv # mp ckan updates the metadata, but we don't want to re-trigger build


# Make a package, using the packages'
# non-versioned names
$(PACKAGE_NAMES): %:$(PACK_DIR)/%.build ; 

# Make all packages 

info:
	@echo ======
	@echo PACKAGE_MARKERS=$(PACKAGE_MARKERS)
	@echo PACKAGE_NAMES=$(PACKAGE_NAMES)

clean: 
	rm -rf $(PACK_DIR)
	mkdir -p $(PACK_DIR)
	find . -name _packages -exec rm -rf {} \; 

clean-cache: 
	rm -rf "$(shell mp info -C)"/library.metatab.org

build: $(PACKAGE_MARKERS) ;

clean-build:
	rm -f $(PACK_DIR)/*.build

s3: $(S3_MARKERS) ;
	
clean-s3:
	rm -f (PACK_DIR)/*.s3
	
ckan: $(CKAN_MARKERS) ;
	

clean-ckan:
	rm -f $(PACK_DIR)/*.ckan
