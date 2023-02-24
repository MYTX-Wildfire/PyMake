
# Class pymake::generators::text\_generator::TextGenerator



[**ClassList**](annotated.md) **>** [**pymake**](namespacepymake.md) **>** [**generators**](namespacepymake_1_1generators.md) **>** [**text\_generator**](namespacepymake_1_1generators_1_1text__generator.md) **>** [**TextGenerator**](classpymake_1_1generators_1_1text__generator_1_1TextGenerator.md)



[More...](#detailed-description)
















## Public Functions

| Type | Name |
| ---: | :--- |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, bool use\_spaces=False, int tab\_size=4) <br> |
|  None | [**append**](#function-append) (self self, str text) <br> |
|  None | [**append\_line**](#function-append_line) (self self, str text) <br> |
|  None | [**apply\_indentation**](#function-apply_indentation) (self self) <br> |
|  bool | [**at\_start\_of\_line**](#function-at_start_of_line) (self self) <br> |
|  None | [**decrease\_indentation\_level**](#function-decrease_indentation_level) (self self, int delta=1) <br> |
|  None | [**finish\_line**](#function-finish_line) (self self) <br> |
|  None | [**increase\_indentation\_level**](#function-increase_indentation_level) (self self, int delta=1) <br> |
|  int | [**indentation\_level**](#function-indentation_level-12) (self self) <br> |
|  None | [**indentation\_level**](#function-indentation_level-22) (self self, int value) <br> |
|  None | [**modify\_indentation\_level**](#function-modify_indentation_level) (self self, int delta) <br> |
|  bool | [**remove\_last\_instance\_of**](#function-remove_last_instance_of) (self self, str text) <br> |
|  str | [**text**](#function-text) (self self) <br> |








# Detailed Description


 


    
## Public Functions Documentation


### function \_\_init\_\_ 


```Python
def pymake::generators::text_generator::TextGenerator::__init__ (
    self self,
    bool use_spaces=False,
    int tab_size=4
) 
```



 


        

### function append 


```Python
None pymake::generators::text_generator::TextGenerator::append (
    self self,
    str text
) 
```



 


        

### function append\_line 


```Python
None pymake::generators::text_generator::TextGenerator::append_line (
    self self,
    str text
) 
```



 


        

### function apply\_indentation 


```Python
None pymake::generators::text_generator::TextGenerator::apply_indentation (
    self self
) 
```



 


        

### function at\_start\_of\_line 


```Python
bool pymake::generators::text_generator::TextGenerator::at_start_of_line (
    self self
) 
```



 


        

### function decrease\_indentation\_level 


```Python
None pymake::generators::text_generator::TextGenerator::decrease_indentation_level (
    self self,
    int delta=1
) 
```



 


        

### function finish\_line 


```Python
None pymake::generators::text_generator::TextGenerator::finish_line (
    self self
) 
```



 


        

### function increase\_indentation\_level 


```Python
None pymake::generators::text_generator::TextGenerator::increase_indentation_level (
    self self,
    int delta=1
) 
```



 


        

### function indentation\_level [1/2]


```Python
int pymake::generators::text_generator::TextGenerator::indentation_level (
    self self
) 
```



 


        

### function indentation\_level [2/2]


```Python
None pymake::generators::text_generator::TextGenerator::indentation_level (
    self self,
    int value
) 
```



 


        

### function modify\_indentation\_level 


```Python
None pymake::generators::text_generator::TextGenerator::modify_indentation_level (
    self self,
    int delta
) 
```



 


        

### function remove\_last\_instance\_of 


```Python
bool pymake::generators::text_generator::TextGenerator::remove_last_instance_of (
    self self,
    str text
) 
```



 


        

### function text 


```Python
str pymake::generators::text_generator::TextGenerator::text (
    self self
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/generators/text_generator.py`