
# Class caller\_info::CallerInfo



[**ClassList**](annotated.md) **>** [**caller\_info**](namespacecaller__info.md) **>** [**CallerInfo**](classcaller__info_1_1CallerInfo.md)



[More...](#detailed-description)
















## Public Functions

| Type | Name |
| ---: | :--- |
|  bool | [**\_\_eq\_\_**](#function-__eq__) (self self, object other) <br> |
|  int | [**\_\_hash\_\_**](#function-__hash__) (self self) <br> |
|  def | [**\_\_init\_\_**](#function-__init__) (self self, Path\|str file\_path, int line\_number) <br> |
|  Path | [**file\_path**](#function-file_path) (self self) <br> |
|  int | [**line\_number**](#function-line_number) (self self) <br> |

## Public Static Functions

| Type | Name |
| ---: | :--- |
|  [**CallerInfo**](classcaller__info_1_1CallerInfo.md) | [**closest\_external\_frame**](#function-closest_external_frame) () <br> |
|  [**CallerInfo**](classcaller__info_1_1CallerInfo.md) | [**from\_stack\_frame**](#function-from_stack_frame) (int offset) <br> |







# Detailed Description


 


    
## Public Functions Documentation


### function \_\_eq\_\_ 


```Python
bool caller_info::CallerInfo::__eq__ (
    self self,
    object other
) 
```



 


        

### function \_\_hash\_\_ 


```Python
int caller_info::CallerInfo::__hash__ (
    self self
) 
```



 


        

### function \_\_init\_\_ 


```Python
def caller_info::CallerInfo::__init__ (
    self self,
    Path|str file_path,
    int line_number
) 
```



 


        

### function file\_path 


```Python
Path caller_info::CallerInfo::file_path (
    self self
) 
```



 


        

### function line\_number 


```Python
int caller_info::CallerInfo::line_number (
    self self
) 
```



 


        
## Public Static Functions Documentation


### function closest\_external\_frame 


```Python
static CallerInfo caller_info::CallerInfo::closest_external_frame () 
```



 


        

### function from\_stack\_frame 


```Python
static CallerInfo caller_info::CallerInfo::from_stack_frame (
    int offset
) 
```



 


        

------------------------------
The documentation for this class was generated from the following file `source/pymake/tracing/caller_info.py`