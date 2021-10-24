from integrations import entities as local_entities
from integrations.backends.mapping import Mapping
from integrations.backends.tally import entities as remote_entities
from integrations.backends.tally import database

mapping = Mapping(
    local_remote_entity={
        local_entities.Currency: remote_entities.Currency,
        local_entities.Location: remote_entities.Location,
        local_entities.Department: remote_entities.Department,
        local_entities.Account: remote_entities.ChartOfAccounts,
        local_entities.Vendor: remote_entities.Vendor,
        local_entities.Bill: remote_entities.VendorBill,
    },
    readonly_entity_lookup={
        remote_entities.Currency: "iso_code",
        remote_entities.Location: "name",
        remote_entities.Department: "name",
        remote_entities.ChartOfAccounts: "number",
    },
    entity_endpoint={
        remote_entities.Currency: "/currencies",
        remote_entities.Location: "/locations",
        remote_entities.Department: "/departments",
        remote_entities.ChartOfAccounts: "/coa",
        remote_entities.Vendor: "/vendors",
        remote_entities.VendorBill: "/vendorbills",
    },
    entity_datastore={
        remote_entities.Currency: database.CurrencyObjectMap,
        remote_entities.Location: database.LocationObjectMap,
        remote_entities.Department: database.DepartmentObjectMap,
        remote_entities.ChartOfAccounts: database.AccountCodeObjectMap,
        remote_entities.Vendor: database.VendorObjectMap,
        remote_entities.VendorBill: database.VendorBillObjectMap,
    },
)
