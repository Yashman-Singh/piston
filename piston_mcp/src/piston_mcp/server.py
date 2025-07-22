from mcp.server.fastmcp import FastMCP

from piston_mcp.api import PistonClient


mcp = FastMCP('piston')


@mcp.tool()
async def run_code(language: str, code: str) -> str:
    async with PistonClient() as client:
        try:
            runtimes_response = await client.runtimes()
        except Exception as e:
            return f'ERROR: failed to get runtimes.\n{repr(e)}'

        language = language.lower()
        version = None

        for runtime in runtimes_response:
            if 'version' not in runtime:
                continue

            if 'language' in runtime and runtime['language'] == language:
                version = runtime['version']
                break

            if 'aliases' in runtime and language in runtime['aliases']:
                version = runtime['version']
                break

        if version is None:
            return 'ERROR: invalid language.'

        try:
            execute_response = await client.execute(
                language=language,
                version=version,
                files=[
                    {
                        'content': code,
                    },
                ],
            )
        except Exception as e:
            return f'ERROR: failed to execute code.\n{repr(e)}'

    output = execute_response.get('run', {}).get('output', '')

    return output


def main():
    mcp.run(transport='stdio')


if __name__ == '__main__':
    main() 