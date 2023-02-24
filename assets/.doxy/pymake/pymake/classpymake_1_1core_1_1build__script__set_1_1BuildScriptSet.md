
# Class pymake::core::build\_script\_set::BuildScriptSet



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**core**](namespacepymake_1_1core.md) **>** [**build\_script\_set**](namespacepymake_1_1core_1_1build__script__set.md) **>** [**BuildScriptSet**](classpymake_1_1core_1_1build__script__set_1_1BuildScriptSet.md)



[More...](#detailed-description)















## Public Static Attributes

| Type | Name |
| ---: | :--- |
|  string | [**EXTERNAL\_GENERATED\_DIR**](#variable-external_generated_dir)   = =  ".external"<br> |

## Public Functions

| Type | Name |
| ---: | :--- |
|  bool | [**\_\_bool\_\_**](#function-__bool__) (self self) <br> |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, Path source\_directory, Path generated\_directory, ICallerInfoFormatter formatter) <br> |
|  int | [**\_\_len\_\_**](#function-__len__) (self self) <br> |
|  def | [**generate**](#function-generate) (self self) <br> |
|  [**BuildScript**](classpymake_1_1core_1_1build__script_1_1BuildScript.md) | [**get\_or\_add\_build\_script**](#function-get_or_add_build_script) (self self, Optional caller\_path=None) <br> |

## Public Static Functions

| Type | Name |
| ---: | :--- |
|  str | [**get\_generated\_build\_script\_name**](#function-get_generated_build_script_name) (Path build\_script\_path) <br> |







# Detailed Description


 


    
## Public Static Attributes Documentation


### variable EXTERNAL\_GENERATED\_DIR 

```Python
string pymake.core.build_script_set.BuildScriptSet::EXTERNAL_GENERATED_DIR;
```



## Public Functions Documentation


### function \_\_bool\_\_ 


```Python
bool pymake::core::build_script_set::BuildScriptSet::__bool__ (
    self self
) 
```



 


        

### function \_\_init\_\_ 


```Python
def pymake::core::build_script_set::BuildScriptSet::__init__ (
    self self,
    Path source_directory,
    Path generated_directory,
    ICallerInfoFormatter formatter
) 
```



 


        

### function \_\_len\_\_ 


```Python
int pymake::core::build_script_set::BuildScriptSet::__len__ (
    self self
) 
```



 


        

### function generate 


```Python
def pymake::core::build_script_set::BuildScriptSet::generate (
    self self
) 
```



 


        

### function get\_or\_add\_build\_script 


```Python
BuildScript pymake::core::build_script_set::BuildScriptSet::get_or_add_build_script (
    self self,
    Optional caller_path=None
) 
```



 


        
## Public Static Functions Documentation


### function get\_generated\_build\_script\_name 


```Python
static str pymake::core::build_script_set::BuildScriptSet::get_generated_build_script_name (
    Path build_script_path
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/core/build_script_set.py`