
# Class pymake::core::preset::Preset



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**core**](namespacepymake_1_1core.md) **>** [**preset**](namespacepymake_1_1core_1_1preset.md) **>** [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md)



[More...](#detailed-description)




Inherits the following classes: ITraced











## Public Static Attributes

| Type | Name |
| ---: | :--- |
|  string | [**CMAKE\_BUILD\_TYPE\_VAR**](#variable-cmake_build_type_var)   = =  "CMAKE\_BUILD\_TYPE"<br> |

## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, str name, Optional desc=None, bool is\_hidden=False, Optional cmake\_generator=None, Optional binary\_path=None, Optional install\_path=None, Optional] cache\_vars=None, Optional] env\_vars=None, Optional\|Sequence inherits=None, bool is\_full\_preset=False) <br> |
|  Dict[str, object] | [**as\_build\_preset**](#function-as_build_preset) (self self, Path source\_dir, Path generated\_dir) <br> |
|  Dict[str, object] | [**as\_configure\_preset**](#function-as_configure_preset) (self self, Path source\_dir, Path generated\_dir) <br> |
|  [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md) | [**as\_full\_preset**](#function-as_full_preset) (self self) <br> |
|  List[[**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md)] | [**base\_presets**](#function-base_presets) (self self) <br> |
|  Optional[str] | [**binary\_dir**](#function-binary_dir-12) (self self) <br> |
|  None | [**binary\_dir**](#function-binary_dir-22) (self self, Optional value) <br> |
|  Dict[str, str] | [**cache\_variables**](#function-cache_variables) (self self) <br> |
|  Optional[str] | [**cmake\_build\_type**](#function-cmake_build_type-12) (self self) <br> |
|  None | [**cmake\_build\_type**](#function-cmake_build_type-22) (self self, Optional value) <br> |
|  Optional[str] | [**description**](#function-description-12) (self self) <br> |
|  None | [**description**](#function-description-22) (self self, Optional value) <br> |
|  Dict[str, str] | [**env\_variables**](#function-env_variables) (self self) <br> |
|  def | [**generate\_trace\_file**](#function-generate_trace_file) (self self, Path output\_path, [**ITraceFileGenerator**](classpymake_1_1generators_1_1trace__file__generator_1_1ITraceFileGenerator.md) generator) <br> |
|  Optional[str] | [**generator**](#function-generator-12) (self self) <br> |
|  None | [**generator**](#function-generator-22) (self self, Optional value) <br> |
|  bool | [**hidden**](#function-hidden-12) (self self) <br> |
|  None | [**hidden**](#function-hidden-22) (self self, bool value) <br> |
|  None | [**inherit\_from**](#function-inherit_from) (self self, [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md) preset) <br> |
|  Optional[str] | [**install\_dir**](#function-install_dir-12) (self self) <br> |
|  None | [**install\_dir**](#function-install_dir-22) (self self, Optional value) <br> |
|  None | [**merge**](#function-merge) (self self, [**Preset**](classpymake_1_1core_1_1preset_1_1Preset.md) preset) <br> |
|  str | [**preset\_name**](#function-preset_name) (self self) <br> |
|  None | [**set\_cache\_variable**](#function-set_cache_variable) (self self, str name, Optional value) <br> |
|  None | [**set\_env\_variable**](#function-set_env_variable) (self self, str name, Optional value) <br> |








# Detailed Description


 


    
## Public Static Attributes Documentation


### variable CMAKE\_BUILD\_TYPE\_VAR 

```Python
string pymake.core.preset.Preset::CMAKE_BUILD_TYPE_VAR;
```



## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::core::preset::Preset::__init__ (
    self self,
    str name,
    Optional desc=None,
    bool is_hidden=False,
    Optional cmake_generator=None,
    Optional binary_path=None,
    Optional install_path=None,
    Optional] cache_vars=None,
    Optional] env_vars=None,
    Optional|Sequence inherits=None,
    bool is_full_preset=False
) 
```



 


        

### function as\_build\_preset 


```Python
Dict[str, object] pymake::core::preset::Preset::as_build_preset (
    self self,
    Path source_dir,
    Path generated_dir
) 
```



 


        

### function as\_configure\_preset 


```Python
Dict[str, object] pymake::core::preset::Preset::as_configure_preset (
    self self,
    Path source_dir,
    Path generated_dir
) 
```



 


        

### function as\_full\_preset 


```Python
Preset pymake::core::preset::Preset::as_full_preset (
    self self
) 
```



 


        

### function base\_presets 


```Python
List[ Preset ] pymake::core::preset::Preset::base_presets (
    self self
) 
```



 


        

### function binary\_dir [1/2]


```Python
Optional[str] pymake::core::preset::Preset::binary_dir (
    self self
) 
```



 


        

### function binary\_dir [2/2]


```Python
None pymake::core::preset::Preset::binary_dir (
    self self,
    Optional value
) 
```



 


        

### function cache\_variables 


```Python
Dict[str, str] pymake::core::preset::Preset::cache_variables (
    self self
) 
```



 


        

### function cmake\_build\_type [1/2]


```Python
Optional[str] pymake::core::preset::Preset::cmake_build_type (
    self self
) 
```



 


        

### function cmake\_build\_type [2/2]


```Python
None pymake::core::preset::Preset::cmake_build_type (
    self self,
    Optional value
) 
```



 


        

### function description [1/2]


```Python
Optional[str] pymake::core::preset::Preset::description (
    self self
) 
```



 


        

### function description [2/2]


```Python
None pymake::core::preset::Preset::description (
    self self,
    Optional value
) 
```



 


        

### function env\_variables 


```Python
Dict[str, str] pymake::core::preset::Preset::env_variables (
    self self
) 
```



 


        

### function generate\_trace\_file 


```Python
def pymake::core::preset::Preset::generate_trace_file (
    self self,
    Path output_path,
    ITraceFileGenerator generator
) 
```



 


        

### function generator [1/2]


```Python
Optional[str] pymake::core::preset::Preset::generator (
    self self
) 
```



 


        

### function generator [2/2]


```Python
None pymake::core::preset::Preset::generator (
    self self,
    Optional value
) 
```



 


        

### function hidden [1/2]


```Python
bool pymake::core::preset::Preset::hidden (
    self self
) 
```



 


        

### function hidden [2/2]


```Python
None pymake::core::preset::Preset::hidden (
    self self,
    bool value
) 
```



 


        

### function inherit\_from 


```Python
None pymake::core::preset::Preset::inherit_from (
    self self,
    Preset preset
) 
```



 


        

### function install\_dir [1/2]


```Python
Optional[str] pymake::core::preset::Preset::install_dir (
    self self
) 
```



 


        

### function install\_dir [2/2]


```Python
None pymake::core::preset::Preset::install_dir (
    self self,
    Optional value
) 
```



 


        

### function merge 


```Python
None pymake::core::preset::Preset::merge (
    self self,
    Preset preset
) 
```



 


        

### function preset\_name 


```Python
str pymake::core::preset::Preset::preset_name (
    self self
) 
```



 


        

### function set\_cache\_variable 


```Python
None pymake::core::preset::Preset::set_cache_variable (
    self self,
    str name,
    Optional value
) 
```



 


        

### function set\_env\_variable 


```Python
None pymake::core::preset::Preset::set_env_variable (
    self self,
    str name,
    Optional value
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/core/preset.py`