using System;
using System.Xml;

public class XXECSharpSample
{
    public void TestLoadXml(string xml)
    {
        XmlDocument doc = new XmlDocument();
        doc.LoadXml(xml);
    }

    public void TestLoad(XmlReader xmlSource)
    {
        XmlDocument doc = new XmlDocument();
        doc.Load(xmlSource);
    }

    public void TestXmlTextReader(string xmlSource)
    {
        XmlTextReader reader = new XmlTextReader(xmlSource);
    }

    public void TestXmlReaderCreate(string xmlSource)
    {
        XmlReader reader = XmlReader.Create(xmlSource);
    }

    public void TestSettingsDtdProcessing()
    {
        XmlReaderSettings settings = new XmlReaderSettings();
        settings.DtdProcessing = DtdProcessing.Parse;
    }

    public void TestSettingsXmlResolver()
    {
        XmlReaderSettings settings = new XmlReaderSettings();
        settings.XmlResolver = new XmlUrlResolver();
    }

    public void TestDocXmlResolver()
    {
        XmlDocument doc = new XmlDocument();
        doc.XmlResolver = new XmlUrlResolver();
    }
}
