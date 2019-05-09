/**
 *  读取xls文件
 */
package main

import (
    "fmt"

    "github.com/tealeg/xlsx"
)


func main() {

    // := 是一个声明语句
    excelFileName := "test.xlsx"
    xlFile, err := xlsx.OpenFile(excelFileName)
    if err != nil {
        fmt.Printf("open failed: %s\n", err)
    }
    // for 循环的 range 格式可以对 slice、map、数组、字符串等进行迭代循环 ,格式如下
    //  for key, value := range oldMap {
    //       newMap[key] = value
    //   }
    for _, sheet := range xlFile.Sheets {
        fmt.Printf("Sheet Name: %s\n", sheet.Name)
        for _, row := range sheet.Rows {
            for _, cell := range row.Cells {
                text := cell.String()
                fmt.Printf("%s\n", text)
            }
        }
    }
}
/**
 * Q: excel.go:6:5: cannot find package "github.com/tealeg/xlsx" in any of:
 * A: $> go get "github.com/tealeg/xlsx"
 *
 * Q:open failed: open test.xlsx: The system cannot find the file specified
 * A: 新建一个文'text.xlsx'文件
 *
 * 
 */