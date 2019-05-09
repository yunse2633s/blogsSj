// go语言让windows发出声音，或者播放音乐的例子：会发出alert警告的声音
// 
// 
package main

import (
"syscall"
"unsafe"
)

func main(){ 

         winSound()

}



// golang 让windows发出警告的声音  todo 需要完善播放mp3之类

func winSound(  )  {

         funInDllFile, err := syscall.LoadLibrary("Winmm.dll") // 调用的dll文件

         if err != nil {

                   print("cant not call : syscall.LoadLibrary , errorInfo :" + err.Error())

         }

         defer syscall.FreeLibrary(funInDllFile)

         // 调用的dll里面的函数是：

         funName := "PlaySound"



         // 注册一长串调用代码，简化为 _win32Fun 变量.

         win32Fun, err := syscall.GetProcAddress(syscall.Handle(funInDllFile), funName) 



         // 通过syscall.Syscall6()去调用win32的xxx函数，因为xxx函数有3个参数,故需取Syscall6才能放得下. 最后的3个参数,设置为0即可

         _, _, err = syscall.Syscall6(

                   uintptr(win32Fun),                                                                             // 调用的函数名

                   3,                                                                                                     // 指明该函数的参数数量

                  

                   uintptr(unsafe.Pointer(syscall.StringToUTF16Ptr("alert") ) ),                    // 该函数的参数1. 可通过msdn查找函数名 查参数含义

                   // SystemStart

                   uintptr( 0 ),                                                                                       // 该函数的参数2.                                  

                   uintptr( 0 ),                                                                                       // 该函数的参数3.               

                                                                

                   0,                                                   

                   0,                                                   

                   0 )             

}