package main

import (
	"reflect"
)

type SafePrototypeUser struct {
	Name  string
	Email string
	Age   int
}

func safeReflectSetField(obj interface{}, fieldName string, value interface{}) {
	allowedFields := map[string]bool{"Name": true, "Email": true, "Age": true}
	if !allowedFields[fieldName] {
		return
	}
	v := reflect.ValueOf(obj).Elem()
	field := v.FieldByName(fieldName)
	field.Set(reflect.ValueOf(value))
}
