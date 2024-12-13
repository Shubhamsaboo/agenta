# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.collect_status_response import CollectStatusResponse
from ..core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from .types.format import Format
from .types.query_traces_response import QueryTracesResponse
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from ..core.client_wrapper import AsyncClientWrapper


class ObservabilityV1Client:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def otlp_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> CollectStatusResponse:
        """
        Status of OTLP endpoint.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability_v_1.otlp_status()
        """
        _response = self._client_wrapper.httpx_client.request(
            "observability/v1/otlp/traces",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def otlp_receiver(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> CollectStatusResponse:
        """
        Receive traces via OTLP.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability_v_1.otlp_receiver()
        """
        _response = self._client_wrapper.httpx_client.request(
            "observability/v1/otlp/traces",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def query_traces(
        self,
        *,
        format: typing.Optional[Format] = None,
        focus: typing.Optional[str] = None,
        oldest: typing.Optional[str] = None,
        newest: typing.Optional[str] = None,
        filtering: typing.Optional[str] = None,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        next: typing.Optional[str] = None,
        stop: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> QueryTracesResponse:
        """
        Query traces, with optional grouping, windowing, filtering, and pagination.

        Parameters
        ----------
        format : typing.Optional[Format]

        focus : typing.Optional[str]

        oldest : typing.Optional[str]

        newest : typing.Optional[str]

        filtering : typing.Optional[str]

        page : typing.Optional[int]

        size : typing.Optional[int]

        next : typing.Optional[str]

        stop : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        QueryTracesResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability_v_1.query_traces()
        """
        _response = self._client_wrapper.httpx_client.request(
            "observability/v1/traces",
            method="GET",
            params={
                "format": format,
                "focus": focus,
                "oldest": oldest,
                "newest": newest,
                "filtering": filtering,
                "page": page,
                "size": size,
                "next": next,
                "stop": stop,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    QueryTracesResponse,
                    parse_obj_as(
                        type_=QueryTracesResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_traces(
        self,
        *,
        node_id: typing.Optional[str] = None,
        node_ids: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> CollectStatusResponse:
        """
        Delete trace.

        Parameters
        ----------
        node_id : typing.Optional[str]

        node_ids : typing.Optional[typing.Union[str, typing.Sequence[str]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        from agenta import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.observability_v_1.delete_traces()
        """
        _response = self._client_wrapper.httpx_client.request(
            "observability/v1/traces",
            method="DELETE",
            params={
                "node_id": node_id,
                "node_ids": node_ids,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncObservabilityV1Client:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def otlp_status(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> CollectStatusResponse:
        """
        Status of OTLP endpoint.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.observability_v_1.otlp_status()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "observability/v1/otlp/traces",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def otlp_receiver(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> CollectStatusResponse:
        """
        Receive traces via OTLP.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.observability_v_1.otlp_receiver()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "observability/v1/otlp/traces",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def query_traces(
        self,
        *,
        format: typing.Optional[Format] = None,
        focus: typing.Optional[str] = None,
        oldest: typing.Optional[str] = None,
        newest: typing.Optional[str] = None,
        filtering: typing.Optional[str] = None,
        page: typing.Optional[int] = None,
        size: typing.Optional[int] = None,
        next: typing.Optional[str] = None,
        stop: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> QueryTracesResponse:
        """
        Query traces, with optional grouping, windowing, filtering, and pagination.

        Parameters
        ----------
        format : typing.Optional[Format]

        focus : typing.Optional[str]

        oldest : typing.Optional[str]

        newest : typing.Optional[str]

        filtering : typing.Optional[str]

        page : typing.Optional[int]

        size : typing.Optional[int]

        next : typing.Optional[str]

        stop : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        QueryTracesResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.observability_v_1.query_traces()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "observability/v1/traces",
            method="GET",
            params={
                "format": format,
                "focus": focus,
                "oldest": oldest,
                "newest": newest,
                "filtering": filtering,
                "page": page,
                "size": size,
                "next": next,
                "stop": stop,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    QueryTracesResponse,
                    parse_obj_as(
                        type_=QueryTracesResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_traces(
        self,
        *,
        node_id: typing.Optional[str] = None,
        node_ids: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> CollectStatusResponse:
        """
        Delete trace.

        Parameters
        ----------
        node_id : typing.Optional[str]

        node_ids : typing.Optional[typing.Union[str, typing.Sequence[str]]]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CollectStatusResponse
            Successful Response

        Examples
        --------
        import asyncio

        from agenta import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )


        async def main() -> None:
            await client.observability_v_1.delete_traces()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "observability/v1/traces",
            method="DELETE",
            params={
                "node_id": node_id,
                "node_ids": node_ids,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CollectStatusResponse,
                    parse_obj_as(
                        type_=CollectStatusResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)