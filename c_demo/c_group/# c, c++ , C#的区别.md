# c, c++ , C#的区别
---------------------------
c 		面向过程式;
c++ 	面向对象;
c#		面向对象;
--------程序结构------------
c: 预处理器指令、mian函数、变量、语句&表达式、注释;
c++：命名空间、main函数
c#: 命名空间、class方法、class属性、main方法、语句&表达式、注释
---------特点----------
c#: 布尔条件、自动垃圾回收、标准库、组件版本、属性和事件、委托和事件管理
易于使用的泛型、索引器、条件编译、多线程、LINQ和Lambda表达式、集成Windows

-------------------
-------- c# 关键字 -----------
abstract	as	base	bool	break	byte	case
catch	char	checked	class	const	continue	decimal
default	delegate	do	double	else	enum	event
explicit	extern	false	finally	fixed	float	for
foreach	goto	if	implicit	in	in (generic
modifier)	int
interface	internal	is	lock	long	namespace	new
null	object	operator	out	out
(generic
modifier)	override	params
private	protected	public	readonly	ref	return	sbyte
sealed	short	sizeof	stackalloc	static	string	struct
switch	this	throw	true	try	typeof	uint
ulong	unchecked	unsafe	ushort	using	virtual	void
volatile	while					
上下文关键字
add	alias	ascending	descending	dynamic	from	get
global	group	into	join	let	orderby	partial
(type)
partial
(method)	remove	select	set
--------- c++ 关键字 62个 ----------
asm	else	new	this
auto	enum	operator	throw
bool	explicit	private	true
break	export	protected	try
case	extern	public	typedef
catch	false	register	typeid
char	float	reinterpret_cast	typename
class	for	return	union
const	friend	short	unsigned
const_cast	goto	signed	using
continue	if	sizeof	virtual
default	inline	static	void
delete	int	static_cast	volatile
do	long	struct	wchar_t
double	mutable	switch	while
dynamic_cast	namespace	template	 
--------- c 关键字 ----------
auto break case char const continue default do
double else enum extern float for goto if int
long register return short signed sizeof static
struct switch typedef unsigned union void volatile
while _Bool	_Complex	_Imaginary	inline	restrict
_Alignas	_Alignof	_Atomic	_Generic	_Noreturn
_Static_assert	_Thread_local
-------------------
-------------------
-------------------
-------------------
1, "hello world"的输出
-------- c -----------

#include <stdio.h>
 
int main()
{
    /* 我的第一个 C 程序 */
    printf("Hello, World! \n"); 
    return 0;
}

-------- c++ -----------
#include <iostream>
using namespace std;
int main()
{
    cout << "Hello, world!" << endl;
    return 0;
}

-------- c# -----------

using System;
namespace HelloWorldApplication
{
    /* 类名为 HelloWorld */
    class HelloWorld
    {
        /* main函数 */
        static void Main(string[] args)
        {
            /* 我的第一个 C# 程序 */
            Console.WriteLine("Hello World!");
            Console.ReadKey();
        }
    }
}
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------
-------------------