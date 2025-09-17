## ```okayql```

```okayql``` is a new comprehensive linting tool for working with Microsoft Sentinel & Defender Advanced Hunting KQL

## Building

To build okayql from sources you will need at least the .NET core SDK v8.0.413. Then follow the steps as described here:

```bash
dotnet build src/Kusto.Language/Kusto.Language.csproj
```

## Usage

To run okayql, you first need to pull the list of tables and their schemas from Microsoft Sentinel or Defender Advanced Hunting. You can do that by following the steps:

```bash
python3 -m pip install azure-identity azure-monitor-query --break-system-packages
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login --use-device-code
```

Once you are authenticated you must follow the steps in schemaindexer.py and then run the script using 

```bash
python3 schemaindexer.py
```

This will produce a json file with all Tables alongside schema which we will inject into okayql for linting purposed. To start the linter please run

```bash
dotnet run --project src/Kusto.Language
```

## Naming

The name ```okayql``` is a playful nod to how it's pronounced: "Oh-Kay-Q-L". Say it out loud, and you'll hear "OK KQL". A fitting name for a tool that helps ensure your KQL is clean, correct, and ready to go

## Microsoft Open Source Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

Resources:

* [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
* [Microsoft Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
* Contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with questions or concerns




