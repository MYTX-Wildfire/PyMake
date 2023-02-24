
# Class pymake::core::cmake::ICMake



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**core**](namespacepymake_1_1core.md) **>** [**cmake**](namespacepymake_1_1core_1_1cmake.md) **>** [**ICMake**](classpymake_1_1core_1_1cmake_1_1ICMake.md)



[More...](#detailed-description)




Inherits the following classes: ABC


Inherited by the following classes: [pymake::core::cmake314::CMake314](classpymake_1_1core_1_1cmake314_1_1CMake314.md),  [pymake::core::cmake325::CMake325](classpymake_1_1core_1_1cmake325_1_1CMake325.md)










## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, [**ECMakeVersion**](classpymake_1_1common_1_1cmake__version_1_1ECMakeVersion.md) minimum\_version, str\|Path source\_directory, str\|Path generated\_directory) <br> |
|  [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md) | [**add\_preset**](#function-add_preset) (self self, str preset\_name) <br> |
|  [**Project**](classpymake_1_1core_1_1project_1_1Project.md) | [**add\_project**](#function-add_project) (self self, str project\_name, [**EProjectLanguage**](classpymake_1_1common_1_1project__language_1_1EProjectLanguage.md)\|Iterable project\_languages) <br> |
|  None | [**build**](#function-build) (self self, bool generate\_first=True, Optional] args=None) <br> |
|  None | [**generate**](#function-generate) (self self, bool generate\_trace\_files=True) <br> |
|  def | [**set\_default\_presets**](#function-set_default_presets) (self self, [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md)\|Iterable presets) <br> |








# Detailed Description


 


    
## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::core::cmake::ICMake::__init__ (
    self self,
    ECMakeVersion minimum_version,
    str|Path source_directory,
    str|Path generated_directory
) 
```



 


        

### function add\_preset 


```Python
Preset pymake::core::cmake::ICMake::add_preset (
    self self,
    str preset_name
) 
```



 


        

### function add\_project 


```Python
Project pymake::core::cmake::ICMake::add_project (
    self self,
    str project_name,
    EProjectLanguage |Iterable project_languages
) 
```



 


        

### function build 


```Python
None pymake::core::cmake::ICMake::build (
    self self,
    bool generate_first=True,
    Optional] args=None
) 
```



 


        

### function generate 


```Python
None pymake::core::cmake::ICMake::generate (
    self self,
    bool generate_trace_files=True
) 
```



 


        

### function set\_default\_presets 


```Python
def pymake::core::cmake::ICMake::set_default_presets (
    self self,
    Preset |Iterable presets
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/core/cmake.py`