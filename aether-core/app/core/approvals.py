import asyncio

class ApprovalManager:
    def __init__(self):
        self.pending = {}

    def create_approval(self, approval_id: str):
        self.pending[approval_id] = asyncio.Event()
        return self.pending[approval_id]

    def approve(self, approval_id: str):
        if approval_id in self.pending:
            self.pending[approval_id].set()
            return True
        return False

    async def wait_for_approval(self, approval_id: str):
        if approval_id in self.pending:
            await self.pending[approval_id].wait()
            del self.pending[approval_id]
            return True
        return False

approval_manager = ApprovalManager()
