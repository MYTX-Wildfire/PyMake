
# Class pymake::core::executable\_target::ExecutableTarget



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**core**](namespacepymake_1_1core.md) **>** [**executable\_target**](namespacepymake_1_1core_1_1executable__target.md) **>** [**ExecutableTarget**](classpymake_1_1core_1_1executable__target_1_1ExecutableTarget.md)



[More...](#detailed-description)




Inherits the following classes: [pymake::core::target::ITarget](classpymake_1_1core_1_1target_1_1ITarget.md)
















## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, [**BuildScriptSet**](classpymake_1_1core_1_1build__script__set_1_1BuildScriptSet.md) build\_scripts, str target\_name) <br> |
|  [**ExecutableTarget**](classpymake_1_1core_1_1executable__target_1_1ExecutableTarget.md) | [**get\_full\_target**](#function-get_full_target) (self self) <br> |

## Public Functions inherited from pymake::core::target::ITarget

See [pymake::core::target::ITarget](classpymake_1_1core_1_1target_1_1ITarget.md)

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, [**BuildScriptSet**](classpymake_1_1core_1_1build__script__set_1_1BuildScriptSet.md) build\_scripts, str target\_name, [**ETargetType**](classpymake_1_1common_1_1target__type_1_1ETargetType.md) target\_type) <br> |
|  None | [**add\_sources**](#function-add_sources) (self self, str\|Iterable sources, [**EScope**](classpymake_1_1common_1_1scope_1_1EScope.md) scope=[**EScope.PRIVATE**](classpymake_1_1common_1_1scope_1_1EScope.md#variable-private)) <br> |
|  def | [**generate\_trace\_file**](#function-generate_trace_file) (self self, Path output\_path, [**ITraceFileGenerator**](classpymake_1_1generators_1_1trace__file__generator_1_1ITraceFileGenerator.md) generator) <br> |
|  [**ITarget**](classpymake_1_1core_1_1target_1_1ITarget.md) | [**get\_full\_target**](#function-get_full_target) (self self) <br> |
|  None | [**install**](#function-install) (self self, Optional install\_path=None) <br> |
|  Optional[str] | [**install\_path**](#function-install_path) (self self) <br> |
|  bool | [**is\_full\_target**](#function-is_full_target) (self self) <br> |
|  bool | [**is\_installed**](#function-is_installed) (self self) <br> |
|  [**ScopedSets**](classpymake_1_1core_1_1scoped__sets_1_1ScopedSets.md)[Path] | [**sources**](#function-sources) (self self) <br> |
|  str | [**target\_name**](#function-target_name) (self self) <br> |
|  [**ETargetType**](classpymake_1_1common_1_1target__type_1_1ETargetType.md) | [**target\_type**](#function-target_type) (self self) <br> |















# Detailed Description


 


    
## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::core::executable_target::ExecutableTarget::__init__ (
    self self,
    BuildScriptSet build_scripts,
    str target_name
) 
```



 


        

### function get\_full\_target 


```Python
ExecutableTarget pymake::core::executable_target::ExecutableTarget::get_full_target (
    self self
) 
```



 


        
Implements [*pymake::core::target::ITarget::get\_full\_target*](classpymake_1_1core_1_1target_1_1ITarget.md#function-get_full_target)


------------------------------
The documentation for this class was generated from the following file `source/pymake/core/executable_target.py`