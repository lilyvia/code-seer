use quick_xml::Reader;
use xml::reader::EventReader;

fn test_xxe(user_xml: &str) {
    let _ = quick_xml::Reader::from_str(user_xml);
    let _ = EventReader::new(user_xml);
    let _ = serde_xml_rs::from_str::<User>(user_xml);
    let _ = roxmltree::Document::parse(user_xml);
}
