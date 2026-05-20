# ZF-GeneBridge
A curated, ZFIN-derived zebrafish gene-expression and annotation database linking stage- and tissue-resolved expression to human disease via orthology and to Gene Ontology annotations 
Last updated 2026‑05‑19


## Overview

This repository contains a structured dataset compiled from the Zebrafish Information Network (ZFIN), a widely used knowledgebase for *Danio rerio* genetics, genomics, development, and disease annotation. The database is designed to support developmental biology, functional genomics, and disease-modeling workflows by bringing together stage-resolved expression information, detailed experimental evidence, orthology-based disease links, and Gene Ontology (GO) annotations in a single source file.

The central source is an Excel workbook composed of multiple sheets, each serving a distinct role in organizing developmental and functional gene information. Together, these sheets allow users to move from high-level expression summaries to evidence-level records and then connect those records to disease relevance and GO-based functional interpretation.

## Data source

All underlying records were obtained from ZFIN, the principal zebrafish model organism database. ZFIN integrates curated information on gene expression, phenotypes, human disease relationships, ontologies, publications, and other core zebrafish research data.

Because the repository redistributes structured information derived from ZFIN, users should cite ZFIN in any publication, report, or analysis that makes use of this dataset. Users should also verify whether newly released ZFIN updates contain records added after 2026-05-19 when performing analyses that require the most current annotations.

## Workbook structure

The source Excel file contains five sheets:

| Sheet name | Description |
|------------|-------------|
| `Stage Order` | Defines the ordered sequence of zebrafish developmental stages used across the repository. This sheet is useful for sorting stage-based analyses and preserving biologically meaningful developmental progression. |
| `wtexpression_Summary` | Contains summarized expression information showing which genes are expressed in which tissues or anatomical regions at specific developmental stages, along with counts of supporting evidence records. |
| `zf_wt_expression` | Contains detailed wild-type expression evidence, including gene name, anatomical location or tissue, developmental stage, assay type, wild-type strain background, and ZFIN publication identifier for each supporting record. |
| `gene2DiseaseOrthology` | Maps zebrafish genes to human disease associations through orthology relationships, enabling translational interpretation of zebrafish genes in a disease context. |
| `GeneOntology` | Provides Gene Ontology annotations for zebrafish genes, supporting functional classification, enrichment analysis, and biological interpretation. |

## Included datasets

### 1. Stage order

The `Stage Order` sheet provides the developmental backbone for the repository by defining the sequence of zebrafish life stages. This is particularly useful for chronological plotting, developmental comparisons, and any analysis that needs standardized stage ordering across multiple sheets.

### 2. Expression summary

The `wtexpression_Summary` sheet offers a compact overview of gene expression across tissues and developmental stages. It is intended for rapid filtering, exploratory analysis, frequency counting, and identification of expression-rich anatomical or developmental windows before consulting the detailed evidence sheet.

### 3. Detailed wild-type expression evidence

The `zf_wt_expression` sheet contains record-level evidence for wild-type zebrafish gene expression. Typical fields include:

- Gene symbol or gene name.
- Anatomical structure, tissue, or expression location.
- Developmental stage.
- Experimental assay used to detect expression.
- Wild-type strain background such as WT, AB, TU, or related designations.
- ZFIN publication ID corresponding to the supporting evidence.

This sheet is intended for users who need traceable evidence, assay-level interpretation, publication linkage, or quality control of individual expression observations.

### 4. Gene-to-disease orthology mapping

The `gene2DiseaseOrthology` sheet connects zebrafish genes to human disease relevance through orthologous relationships. This makes the repository useful for translational research questions, candidate gene prioritization, disease-model exploration, and hypothesis generation in comparative biology.

### 5. Gene Ontology annotation

The `GeneOntology` sheet adds functional context by annotating zebrafish genes with GO terms. These annotations can be used to group genes by biological process, molecular function, or cellular component, and they can support downstream enrichment or pathway-style analyses.

## What this repository enables

This repository is useful for workflows such as:

- Identifying where and when a zebrafish gene is expressed during development.
- Comparing tissue-specific expression patterns across developmental stages.
- Reviewing the experimental evidence supporting a reported expression pattern.
- Linking zebrafish genes to human disease associations through orthology.
- Adding GO-based functional interpretation to genes of interest.
- Building candidate gene lists for developmental, metabolic, or disease-focused studies.
- Creating reproducible pipelines that combine expression, disease, and functional annotation layers.

## Recommended use cases

This repository may be especially useful for:

- Developmental biologists studying stage-specific and tissue-specific expression patterns.
- Disease model researchers interested in zebrafish-to-human translational relevance.
- Functional genomics projects requiring integrated expression and GO annotation.
- Bioinformatics workflows that need a precompiled workbook rather than repeated direct extraction from source databases.
- Educational or exploratory analyses where both summary-level and evidence-level data are needed.

## Suggested workflow

A practical way to use the workbook is:

1. Use `Stage Order` to define the developmental sequence for plotting or sorting.
2. Start with `20260518_wtexpression_Summary` to identify genes, tissues, or stages of interest.
3. Move to `20260518_zf_wt_expression` to inspect evidence-level details, assays, strains, and publication IDs.
4. Join genes of interest with `20260519_gene2DiseaseOrthology` to explore translational disease relevance.
5. Add `20260519_GeneOntology` to interpret the functional roles of selected genes.

## Provenance and versioning

The current workbook version was last updated on **2026-05-19**. Data provenance is rooted in ZFIN, and version tracking should be maintained whenever the workbook is refreshed so that downstream analyses remain reproducible and comparable across releases.

A recommended versioning practice is to retain the source date in filenames and repository release notes. This helps users distinguish between annotation snapshots and track changes as ZFIN data evolve over time.

## Citation and attribution

Please cite ZFIN when using this repository in manuscripts, presentations, reports, or software pipelines because the underlying records were obtained from the ZFIN knowledgebase. The ZFIN database has been described as the zebrafish model organism database and knowledgebase for *Danio rerio* research.

Suggested attribution text:

> Data in this repository were compiled from the Zebrafish Information Network (ZFIN) and organized into a local resource integrating developmental stage order, wild-type gene expression, disease associations via orthology, and Gene Ontology annotations.

## Data quality notes

Users should keep in mind that the expression summary sheet provides aggregated counts, whereas the detailed expression sheet contains evidence-level observations. Analyses that depend on assay type, publication source, or strain-specific context should rely on the detailed sheet rather than summary-level counts alone.

Orthology-based disease mapping is useful for prioritization and interpretation, but it should not be treated as direct proof of conserved disease mechanism in zebrafish. Functional validation and literature review remain important when translating orthology relationships into biological conclusions.

## Reproducibility

For reproducible use, it is helpful to document:

- The exact workbook filename and date.
- Any filtering applied before analysis.
- The join keys used between expression, disease, and GO sheets.
- Whether analyses were performed on summary-level or evidence-level data.
- The version of downstream scripts or notebooks used to parse the workbook.

These practices make it easier to compare results across updates and ensure that analyses can be revisited later without ambiguity.

## Future extensions

Potential future additions to this repository include:

- Parsed CSV exports for each sheet.
- A formal data dictionary describing each column.
- Validation scripts for schema consistency.
- Simple search utilities for genes, tissues, stages, or diseases.
- Visualization notebooks for developmental expression heatmaps or disease-linked gene summaries.
- Release-tagged snapshots aligned to future ZFIN updates.
