from api.v1.operation.schemas import OperationModelAddDTO
from repositories.base_repository import AbstractRepository

class OperationService:
    def __init__(self, operation_rep: AbstractRepository):
        self.operation_rep: AbstractRepository = operation_rep()

    async def add_operation(self, operation: OperationModelAddDTO):
        operation_dict = operation.model_dump()
        new_operation_id = await self.operation_rep.add_one(data=operation_dict)
        return new_operation_id
    
    async def get_operation(self, operation_id: int):
        operation = await self.operation_rep.get_one(operation_id)
        return operation