
# Class pymake::generators::cmake\_generator::CMakeGenerator



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**generators**](namespacepymake_1_1generators.md) **>** [**cmake\_generator**](namespacepymake_1_1generators_1_1cmake__generator.md) **>** [**CMakeGenerator**](classpymake_1_1generators_1_1cmake__generator_1_1CMakeGenerator.md)



[More...](#detailed-description)
















## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, ICallerInfoFormatter formatter, bool use\_spaces=False, int tab\_size=4) <br> |
|  str | [**generate**](#function-generate) (self self) <br> |
|  [**CMakeMethodBuilder**](classpymake_1_1generators_1_1cmake__method__builder_1_1CMakeMethodBuilder.md) | [**open\_method\_block**](#function-open_method_block) (self self, str method\_name) <br> |
|  None | [**write\_file**](#function-write_file) (self self, str\|Path output\_path) <br> |








# Detailed Description


 


    
## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::generators::cmake_generator::CMakeGenerator::__init__ (
    self self,
    ICallerInfoFormatter formatter,
    bool use_spaces=False,
    int tab_size=4
) 
```



 


        

### function generate 


```Python
str pymake::generators::cmake_generator::CMakeGenerator::generate (
    self self
) 
```



 


        

### function open\_method\_block 


```Python
CMakeMethodBuilder pymake::generators::cmake_generator::CMakeGenerator::open_method_block (
    self self,
    str method_name
) 
```



 


        

### function write\_file 


```Python
None pymake::generators::cmake_generator::CMakeGenerator::write_file (
    self self,
    str|Path output_path
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/generators/cmake_generator.py`