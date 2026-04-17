using System;
using System.Collections.Generic;
using System.Reflection;

class SafePrototypePollutionCsharp {
    private static readonly HashSet<string> AllowedProperties = new HashSet<string> { "Name", "Email", "Age" };
    private static readonly HashSet<string> AllowedMethods = new HashSet<string> { "GetName", "GetEmail" };

    public void SafeSetProperty(object obj, string propertyName, object value) {
        if (AllowedProperties.Contains(propertyName)) {
            var prop = obj.GetType().GetProperty(propertyName);
            prop.SetValue(obj, value);
        }
    }

    public void SafeInvokeMethod(object obj, string methodName) {
        if (AllowedMethods.Contains(methodName)) {
            var method = obj.GetType().GetMethod(methodName);
            method.Invoke(obj, null);
        }
    }
}
