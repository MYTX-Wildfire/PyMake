
# Class pymake::core::project::Project



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**core**](namespacepymake_1_1core.md) **>** [**project**](namespacepymake_1_1core_1_1project.md) **>** [**Project**](classpymake_1_1core_1_1project_1_1Project.md)



[More...](#detailed-description)




Inherits the following classes: ITraced












## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, [**BuildScriptSet**](classpymake_1_1core_1_1build__script__set_1_1BuildScriptSet.md) build\_scripts, str project\_name, [**EProjectLanguage**](classpymake_1_1common_1_1project__language_1_1EProjectLanguage.md)\|Iterable project\_languages) <br> |
|  [**ExecutableTarget**](classpymake_1_1core_1_1executable__target_1_1ExecutableTarget.md) | [**add\_executable**](#function-add_executable) (self self, str target\_name) <br> |
|  Iterable[[**EProjectLanguage**](classpymake_1_1common_1_1project__language_1_1EProjectLanguage.md)] | [**project\_languages**](#function-project_languages) (self self) <br> |
|  str | [**project\_name**](#function-project_name) (self self) <br> |








# Detailed Description


 


    
## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::core::project::Project::__init__ (
    self self,
    BuildScriptSet build_scripts,
    str project_name,
    EProjectLanguage |Iterable project_languages
) 
```



 


        

### function add\_executable 


```Python
ExecutableTarget pymake::core::project::Project::add_executable (
    self self,
    str target_name
) 
```



 


        

### function project\_languages 


```Python
Iterable[ EProjectLanguage ] pymake::core::project::Project::project_languages (
    self self
) 
```



 


        

### function project\_name 


```Python
str pymake::core::project::Project::project_name (
    self self
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/core/project.py`