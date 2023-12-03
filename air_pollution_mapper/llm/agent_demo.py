from air_pollution_mapper.llm.utils import load_secrets as llm_load_secrets
from air_pollution_mapper.api_caller.utils import load_secrets as gmaps_load_secrets
from air_pollution_mapper.llm.AirQualityAgent import AirQualityAgent


def main():
    secrets_llm = llm_load_secrets()
    secrets_gmaps = gmaps_load_secrets()
    parser = AirQualityAgent(
        openai_api_key=secrets_llm["OPENAI_API_KEY"],
        google_maps_api_key=secrets_gmaps["GOOGLE_MAPS_API_KEY"],
    )

    while True:
        inputtext = input("Enter query (Q to quit): ")
        if inputtext == "Q":
            break
        else:
            response, df, health_suggestion, map = parser.parse(inputtext)
            print(df.head())


if __name__ == "__main__":
    main()
