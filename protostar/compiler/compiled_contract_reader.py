import json
from pathlib import Path
from typing import Optional

from starkware.starknet.public.abi import AbiType
from starkware.starknet.services.api.contract_class import ContractClass


class CompiledContractReader:
    @staticmethod
    def load_contract(contract_path: Path) -> ContractClass:
        contract_class_str = contract_path.read_bytes()
        return ContractClass.deserialize(contract_class_str)

    def load_abi_from_contract_path(self, contract_path: Path) -> Optional[AbiType]:
        abi_path = self._get_abi_path_from_contract_path(contract_path)
        return self._load_abi(abi_path)

    @staticmethod
    def _get_abi_path_from_contract_path(contract_path: Path) -> Path:
        return contract_path.parent / f"{contract_path.stem}_abi.json"

    @staticmethod
    def _load_abi(abi_path: Path) -> Optional[AbiType]:
        assert abi_path.suffix == ".json"
        return json.loads(abi_path.read_text())
