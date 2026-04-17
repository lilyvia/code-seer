// Safe: Avoid XML parsers for untrusted data
// Use JSON or manual validation instead

pub fn safe_validate_xml_length(xml: &str) -> Result<(), &'static str> {
    if xml.len() > 1024 * 1024 {
        return Err("XML too large");
    }
    Ok(())
}
