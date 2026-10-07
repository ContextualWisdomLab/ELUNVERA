//! Versioned domain contracts shared by ELUNVERA foundation modules.

#![forbid(unsafe_code)]
#![deny(missing_docs)]

use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::str::FromStr;

/// The domain-contract version supported by this foundation slice.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ContractVersion;

impl Display for ContractVersion {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("0.1.0")
    }
}

impl FromStr for ContractVersion {
    type Err = UnsupportedContractVersion;

    fn from_str(candidate: &str) -> Result<Self, Self::Err> {
        if candidate == "0.1.0" {
            Ok(Self)
        } else {
            Err(UnsupportedContractVersion(candidate.to_owned()))
        }
    }
}

/// Error returned when a consumer requests an unsupported contract version.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct UnsupportedContractVersion(String);

impl Display for UnsupportedContractVersion {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("unsupported domain contract version: ")?;
        formatter.write_str(&self.0)
    }
}

impl Error for UnsupportedContractVersion {}
