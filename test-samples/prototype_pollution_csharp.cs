using System;
using System.Collections.Generic;
using System.Reflection;

class PrototypePollutionCsharp {
    public void VulnerableSetProperty(object obj, string userPropertyName, object userValue) {
        obj.GetType().GetProperty(userPropertyName).SetValue(obj, userValue);
    }

    public void VulnerableSetField(object obj, string userFieldName, object userValue) {
        obj.GetType().GetField(userFieldName).SetValue(obj, userValue);
    }

    public void VulnerableInvokeMethod(object obj, string userMethodName) {
        obj.GetType().GetMethod(userMethodName).Invoke(obj, null);
    }
}
