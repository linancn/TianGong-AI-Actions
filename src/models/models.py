from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional



class Sources(str, Enum):
    Agriculture_ecosystems_environment = "AGRICULTURE, ECOSYSTEMS & ENVIRONMENT"
    Annual_review_of_ecologyevolutionand_systematics = "ANNUAL REVIEW OF ECOLOGY, EVOLUTION, AND SYSTEMATICS"
    Annual_review_of_environment_and_resources = "ANNUAL REVIEW OF ENVIRONMENT AND RESOURCES"
    Applied_catalysis_b_environmental = "APPLIED CATALYSIS B: ENVIRONMENTAL"
    Biogeosciences = "BIOGEOSCIENCES"
    Biological_conservation = "BIOLOGICAL CONSERVATION"
    Biotechnology_advances = "BIOTECHNOLOGY ADVANCES"
    Conservation_biology = "CONSERVATION BIOLOGY"
    Conservation_letters = "CONSERVATION LETTERS"
    Critical_reviews_in_environmental_science_and_technology = "CRITICAL REVIEWS IN ENVIRONMENTAL SCIENCE AND TECHNOLOGY"
    Diversity_and_distributions = "DIVERSITY AND DISTRIBUTIONS"
    Ecography = "ECOGRAPHY"
    Ecological_applications = "ECOLOGICAL APPLICATIONS"
    Ecological_economics = "ECOLOGICAL ECONOMICS"
    Ecological_monographs = "ECOLOGICAL MONOGRAPHS"
    Ecology = "ECOLOGY"
    Ecology_letters = "ECOLOGY LETTERS"
    Economic_systems_research = "ECONOMIC SYSTEMS RESEARCH"
    Ecosystem_health_and_sustainability = "ECOSYSTEM HEALTH AND SUSTAINABILITY"
    Ecosystem_services = "ECOSYSTEM SERVICES"
    Ecosystems = "ECOSYSTEMS"
    Energy_environmental_science = "ENERGY & ENVIRONMENTAL SCIENCE"
    Environment_international = "ENVIRONMENT INTERNATIONAL"
    Environmental_chemistry_letters = "ENVIRONMENTAL CHEMISTRY LETTERS"
    Environmental_health_perspectives = "ENVIRONMENTAL HEALTH PERSPECTIVES"
    Environmental_pollution = "ENVIRONMENTAL POLLUTION"
    Environmental_science_technology = "ENVIRONMENTAL SCIENCE & TECHNOLOGY"
    Environmental_science_technology_letters = "ENVIRONMENTAL SCIENCE & TECHNOLOGY LETTERS"
    Environmental_science_and_ecotechnology = "ENVIRONMENTAL SCIENCE AND ECOTECHNOLOGY"
    Environmental_science_and_pollution_research = "ENVIRONMENTAL SCIENCE AND POLLUTION RESEARCH"
    Evolution = "EVOLUTION"
    Forest_ecosystems = "FOREST ECOSYSTEMS"
    Frontiers_in_ecology_and_the_environment = "FRONTIERS IN ECOLOGY AND THE ENVIRONMENT"
    Frontiers_of_environmental_science_engineering = "FRONTIERS OF ENVIRONMENTAL SCIENCE & ENGINEERING"
    Functional_ecology = "FUNCTIONAL ECOLOGY"
    Global_change_biology = "GLOBAL CHANGE BIOLOGY"
    Global_ecology_and_biogeography = "GLOBAL ECOLOGY AND BIOGEOGRAPHY"
    Global_environmental_change = "GLOBAL ENVIRONMENTAL CHANGE"
    International_soil_and_water_conservation_research = "INTERNATIONAL SOIL AND WATER CONSERVATION RESEARCH"
    Journal_of_animal_ecology = "JOURNAL OF ANIMAL ECOLOGY"
    Journal_of_applied_ecology = "JOURNAL OF APPLIED ECOLOGY"
    Journal_of_biogeography = "JOURNAL OF BIOGEOGRAPHY"
    Journal_of_cleaner_production = "JOURNAL OF CLEANER PRODUCTION"
    Journal_of_ecology = "JOURNAL OF ECOLOGY"
    Journal_of_environmental_informatics = "JOURNAL OF ENVIRONMENTAL INFORMATICS"
    Journal_of_environmental_management = "JOURNAL OF ENVIRONMENTAL MANAGEMENT"
    Journal_of_hazardous_materials = "JOURNAL OF HAZARDOUS MATERIALS"
    Journal_of_industrial_ecology = "JOURNAL OF INDUSTRIAL ECOLOGY"
    Journal_of_plant_ecology = "JOURNAL OF PLANT ECOLOGY"
    Landscape_and_urban_planning = "LANDSCAPE AND URBAN PLANNING"
    Landscape_ecology = "LANDSCAPE ECOLOGY"
    Methods_in_ecology_and_evolution = "METHODS IN ECOLOGY AND EVOLUTION"
    Microbiome = "MICROBIOME"
    Molecular_ecology = "MOLECULAR ECOLOGY"
    Nature = "NATURE"
    Nature_climate_change = "NATURE CLIMATE CHANGE"
    Nature_communications = "NATURE COMMUNICATIONS"
    Nature_ecology_evolution = "NATURE ECOLOGY & EVOLUTION"
    Nature_energy = "NATURE ENERGY"
    Nature_reviews_earth_environment = "NATURE REVIEWS EARTH & ENVIRONMENT"
    Nature_sustainability = "NATURE SUSTAINABILITY"
    One_earth = "ONE EARTH"
    People_and_nature = "PEOPLE AND NATURE"
    Proceedings_of_the_national_academy_of_sciences = "PROCEEDINGS OF THE NATIONAL ACADEMY OF SCIENCES"
    Proceedings_of_the_royal_society_b_biological_sciences = "PROCEEDINGS OF THE ROYAL SOCIETY B: BIOLOGICAL SCIENCES"
    Renewable_and_sustainable_energy_reviews = "RENEWABLE AND SUSTAINABLE ENERGY REVIEWS"
    Resourcesconservation_and_recycling = "RESOURCES, CONSERVATION AND RECYCLING"
    Reviews_in_environmental_science_and_biotechnology = "REVIEWS IN ENVIRONMENTAL SCIENCE AND BIO/TECHNOLOGY"
    Science = "SCIENCE"
    Science_advances = "SCIENCE ADVANCES"
    Science_of_the_total_environment = "SCIENCE OF THE TOTAL ENVIRONMENT"
    Scientific_data = "SCIENTIFIC DATA"
    Sustainable_cities_and_society = "SUSTAINABLE CITIES AND SOCIETY"
    Sustainable_materials_and_technologies = "SUSTAINABLE MATERIALS AND TECHNOLOGIES"
    Sustainable_production_and_consumption = "SUSTAINABLE PRODUCTION AND CONSUMPTION"
    The_american_naturalist = "THE AMERICAN NATURALIST"
    The_international_journal_of_life_cycle_assessment = "THE INTERNATIONAL JOURNAL OF LIFE CYCLE ASSESSMENT"
    The_isme_journal = "THE ISME JOURNAL"
    The_lancet_planetary_health = "THE LANCET PLANETARY HEALTH"
    Trends_in_ecology_evolution = "TRENDS IN ECOLOGY & EVOLUTION"
    Waste_management = "WASTE MANAGEMENT"
    Water_research = "WATER RESEARCH"


class DocumentMetadata(BaseModel):
    source: Optional[str] = None
    source_id: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[float] = None
    author: Optional[str] = None


class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[List[float]] = None


class DocumentChunkNeat(BaseModel):
    text: str
    source: str


class DocumentChunkWithScore(DocumentChunk):
    score: float


class DocumentChunkWithScoreNeat(DocumentChunkNeat):
    score: float


class Document(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[DocumentMetadata] = None


class DocumentWithChunks(Document):
    chunks: List[DocumentChunk]


class DocumentMetadataFilter(BaseModel):
    document_id: Optional[str] = None
    source: Optional[Sources] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format

    def __init__(self, **data):
        if 'source' in data:
            source_value = data['source'].upper()
            for source in Sources:
                if source.value.upper() == source_value:
                    data['source'] = source
                    break
        super().__init__(**data)


class Query(BaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 16


class QueryWithEmbedding(Query):
    embedding: List[float]


class QueryResult(BaseModel):
    query: str
    results: List[DocumentChunkWithScore]


class QueryResultNeat(BaseModel):
    query: str
    results: List[DocumentChunkWithScoreNeat]

class LCAProcessQuery(BaseModel):
    query: str

class LCAProcessResponse(BaseModel):
    results: str