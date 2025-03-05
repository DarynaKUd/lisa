from dataclasses import dataclass, field
from typing import Any, Optional, Type
from logging import Logger

from dataclasses_json import dataclass_json, LetterCase, config

from lisa import schema
from lisa.node import Node, quick_connect
from lisa.transformer import Transformer
from lisa.util import field_metadata, LisaException


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeploymentTransformerSchema(schema.Transformer):
    """Schema for DeploymentTransformer configuration"""
    # SSH connection information to the node
    connection: Optional[schema.RemoteNode] = field(
        default=None,
        metadata=field_metadata(
            required=False,
            description="SSH connection details for the target node"
        )
    )

    def validate(self) -> None:
        """Validate the schema configuration"""
        super().validate()
        if self.connection:
            self.connection.validate()


class DeploymentTransformer(Transformer):
    """
    Transformer for handling deployment operations on a remote node
    
    This class manages the connection and deployment process to a target node,
    either using a pre-existing node or establishing a new connection.
    """
    
    __type_name = "deployment"

    def __init__(
        self,
        runbook: DeploymentTransformerSchema,
        node: Optional[Node] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the DeploymentTransformer
        
        Args:
            runbook: Configuration schema for the transformer
            node: Optional pre-existing node connection
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Raises:
            LisaException: If connection cannot be established when required
        """
        super().__init__(runbook, *args, **kwargs)
        self._runbook: DeploymentTransformerSchema = runbook
        self._logger: Logger = self._log
        
        try:
            if node:
                self._node = node
                self._logger.debug(f"Using
