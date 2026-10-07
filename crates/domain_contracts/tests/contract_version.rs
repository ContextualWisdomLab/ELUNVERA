use domain_contracts::ContractVersion;

#[test]
fn parses_and_displays_the_supported_contract_version() {
    let version = "0.1.0".parse::<ContractVersion>().expect("supported version");

    assert_eq!(version.to_string(), "0.1.0");
}

#[test]
fn rejects_an_unsupported_contract_version() {
    let error = "0.2.0"
        .parse::<ContractVersion>()
        .expect_err("unsupported versions must fail closed");

    assert_eq!(error.to_string(), "unsupported domain contract version: 0.2.0");
}
