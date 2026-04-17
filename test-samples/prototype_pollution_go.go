package main

import (
	"reflect"
)

type PrototypeUser struct {
	Name  string
	Email string
	Age   int
}

func vulnerableReflectSetField(obj interface{}, fieldName string, value interface{}) {
	reflect.ValueOf(obj).Elem().FieldByName(fieldName).Set(reflect.ValueOf(value))
}

func vulnerableReflectSetFieldDirect(obj interface{}, userFieldName string, userValue interface{}) {
	reflect.ValueOf(obj).Elem().FieldByName(userFieldName).Set(reflect.ValueOf(userValue))
}
