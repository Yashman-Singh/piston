from typing import NamedTuple
import httpx


DEFAULT_RUNTIMES_URL = 'http://localhost:2000/api/v2/runtimes'
DEFAULT_EXECUTE_URL = 'http://localhost:2000/api/v2/execute'


class Runtime(NamedTuple):
    language: str
    version: str
    aliases: list[str]


class File:
    name: str | None
    content: str
    encoding: str | None


class ExecuteStageResults(NamedTuple):
    stdout: str
    stderr: str
    output: str
    code: int | None
    signal: str | None
    message: str | None
    status: str | None
    cpu_time: int | None
    wall_time: int | None
    memory: int | None


class ExecuteResults(NamedTuple):
    language: str
    version: str
    compile: ExecuteStageResults | None
    run: ExecuteStageResults


class PistonClient:
    def __init__(
        self,
        runtimes_url: str = DEFAULT_RUNTIMES_URL,
        execute_url: str = DEFAULT_EXECUTE_URL,
        timeout: float = 10.0,
    ):
        self.runtimes_url = runtimes_url
        self.execute_url = execute_url
        self.client = httpx.AsyncClient(timeout=timeout)

    async def runtimes(self) -> list[Runtime]:
        response = await self.client.get(url=self.runtimes_url)
        response.raise_for_status()
        return response.json()

    async def execute(
        self,
        language: str,
        version: str,
        files: list[File],
        stdin: str | None = None,
        args: list[str] | None = None,
        compile_timeout: int | None = None,
        run_timeout: int | None = None,
        compile_cpu_time: int | None = None,
        run_cpu_time: int | None = None,
        compile_memory_limit: int | None = None,
        run_memory_limit: int | None = None,
    ) -> ExecuteResults:
        if len(files) < 1:
            raise ValueError('No files provided')

        validated_files = []
        for file in files:
            if 'content' not in file:
                raise ValueError('No content in file')

            validated_file = {
                'content': file['content'],
            }

            if 'name' in file:
                validated_file['name'] = file['name']

            if 'encoding' in file:
                validated_file['encoding'] = file['encoding']

            validated_files.append(validated_file)

        data = {
            'language': language,
            'version': version,
            'files': validated_files,
        }

        if stdin is not None:
            data['stdin'] = stdin

        if args is not None:
            data['args'] = args

        if compile_timeout is not None:
            data['compile_timeout'] = compile_timeout

        if run_timeout is not None:
            data['run_timeout'] = run_timeout

        if compile_cpu_time is not None:
            data['compile_cpu_time'] = compile_cpu_time

        if run_cpu_time is not None:
            data['run_cpu_time'] = run_cpu_time

        if compile_memory_limit is not None:
            data['compile_memory_limit'] = compile_memory_limit

        if run_memory_limit is not None:
            data['run_memory_limit'] = run_memory_limit

        response = await self.client.post(
            url=self.execute_url,
            json=data,
        )
        response.raise_for_status()

        return response.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close() 