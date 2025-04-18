from dataclasses import field
from pydantic.dataclasses import dataclass

from .utils import null_if_empty, to_float

@dataclass
class PatientRecord:
    id: str = field(metadata={'mapped_to': 'ID'})
    current_diagnose: int = field(metadata={'mapped_to': 'DIAGNOSI_ATTUALE', 'transform': lambda x: int(x)})
    age: int = field(metadata={'mapped_to': 'ETA\'', 'transform': lambda x: int(x)})
    sex: bool = field(metadata={'mapped_to': 'SESSO', 'transform': lambda x: bool(x)})
    right_handed: bool | None = field(metadata={'mapped_to': 'DESTRIMANE/MANCINO', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    schooling: int | None = field(metadata={'mapped_to': 'SCOLARITA\'', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    egfr: int | None = field(metadata={'mapped_to': 'eGFR', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    first_visit: str | None = field(metadata={'mapped_to': '1° visita', 'transform': lambda x: null_if_empty(x)})
    diagnose_date: str | None = field(metadata={'mapped_to': 'Data diagnosi', 'transform': lambda x: null_if_empty(x)})
    a: bool | None = field(metadata={'mapped_to': 'A', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    t: bool | None = field(metadata={'mapped_to': 'T', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    n: bool | None = field(metadata={'mapped_to': 'N', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    memoria: bool | None = field(metadata={'mapped_to': 'memoria', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    memoria_esordio: str | None = field(metadata={'mapped_to': 'memoria esordio', 'transform': lambda x: null_if_empty(x)})
    fx_esecutive: bool | None = field(metadata={'mapped_to': 'fx esecutive', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    fx_esecutive_esordio: str | None = field(metadata={'mapped_to': 'fx esecutive esordio', 'transform': lambda x: null_if_empty(x)}) # TODO: prime righe int, poi date
    fx_visuo_spaziali: bool | None = field(metadata={'mapped_to': 'fx visuo-spaziali', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    fx_visuo_spaziali_esordio: str | None = field(metadata={'mapped_to': 'fx visuo-spaziali esordio', 'transform': lambda x: null_if_empty(x)})
    linguaggio: bool | None = field(metadata={'mapped_to': 'linguaggio', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    linguaggio_esordio: str | None = field(metadata={'mapped_to': 'linguaggio esordio', 'transform': lambda x: null_if_empty(x)})
    fx_pratto_gnosiche: bool | None = field(metadata={'mapped_to': 'fx pratto-gnosiche', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    fx_pratto_gnosiche_esordio: str | None = field(metadata={'mapped_to': 'fx pratto-gnosiche esordio', 'transform': lambda x: null_if_empty(x)})
    social_cognition: bool | None = field(metadata={'mapped_to': 'social cognition', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    social_cognition_esordio: str | None = field(metadata={'mapped_to': 'social cognition esordio', 'transform': lambda x: null_if_empty(x)})
    comportamento: bool | None = field(metadata={'mapped_to': 'Comportamento', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    comportamento_esordio: str | None = field(metadata={'mapped_to': 'Comportamento esordio', 'transform': lambda x: null_if_empty(x)})
    extrapiramidale: bool | None = field(metadata={'mapped_to': 'Extrapiramidale', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    adl: int | None = field(metadata={'mapped_to': 'ADL', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    iadl: float | None = field(metadata={'mapped_to': 'IADL', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    cdr: float | None = field(metadata={'mapped_to': 'CDR', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    cdr_sob: str | None = field(metadata={'mapped_to': 'CDR-SOB'})
    tau_totale_liquor: int | None = field(metadata={'mapped_to': 'Tau Totale Liquor', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    ptau_181_liquor: float | None = field(metadata={'mapped_to': 'pTAU-181 Liquor', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    ttau_ptau: float | None = field(metadata={'mapped_to': 'tTAU/pTAU', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    mta: int | None = field(metadata={'mapped_to': 'MTA', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    fazekas: int | None = field(metadata={'mapped_to': 'FAZEKAS', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    koedam: int | None = field(metadata={'mapped_to': 'KOEDAM', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    gca: int | None = field(metadata={'mapped_to': 'GCA', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    vascular: int | None = field(metadata={'mapped_to': 'VASCULAR', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    pet_fdg: bool | None = field(metadata={'mapped_to': 'PET-FDG', 'transform': lambda x: null_if_empty(x, lambda v: bool(v))})
    spect: int | None = field(metadata={'mapped_to': 'SPECT', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    pet_a: int | None = field(metadata={'mapped_to': 'PET-A?', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    mmse_raw: int | None = field(metadata={'mapped_to': 'MMSE [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    mmse_corr: float | None = field(metadata={'mapped_to': 'MMSE [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fab_raw: int | None = field(metadata={'mapped_to': 'FAB [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    fab_corr: float | None = field(metadata={'mapped_to': 'FAB [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    memoria_di_prosa_immediata_raw: float | None = field(metadata={'mapped_to': 'memoria di prosa - immediata [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    memoria_di_prosa_immediata_corr: float | None = field(metadata={'mapped_to': 'memoria di prosa - immediata [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    memoria_di_prosa_differita_raw: float | None = field(metadata={'mapped_to': 'memoria di prosa - differita [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    memoria_di_prosa_differita_corr: float | None = field(metadata={'mapped_to': 'memoria di prosa - differita [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fcsrt_immediate_free_recall_raw: int | None = field(metadata={'mapped_to': 'FCSRT - Immediate free recall [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    fcsrt_immediate_free_recall_corr: float | None = field(metadata={'mapped_to': 'FCSRT - Immediate free recall [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fcsrt_delayed_free_recall_raw: int | None = field(metadata={'mapped_to': 'FCSRT - Delayed free recall [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    fcsrt_delayed_free_recall_corr: float | None = field(metadata={'mapped_to': 'FCSRT - Delayed free recall [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fcsrt_isc: float | None = field(metadata={'mapped_to': 'FCSRT - ISC', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fcsrt_itr: int | None = field(metadata={'mapped_to': 'FCSRT - ITR', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    fcsrt_dtr: int | None = field(metadata={'mapped_to': 'FCSRT - DTR', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    ravlt_immediato_raw: int | None = field(metadata={'mapped_to': 'RAVLT - Immediato [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    ravlt_immediato_corr: float | None = field(metadata={'mapped_to': 'RAVLT - Immediato [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    ravlt_differito_raw: int | None = field(metadata={'mapped_to': 'RAVLT - Differito [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    ravlt_differito_corr: float | None = field(metadata={'mapped_to': 'RAVLT - Differito [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    ravlt_recognition: float | None = field(metadata={'mapped_to': 'RAVLT - Recognition', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    digit_span_diretto_raw: int | None = field(metadata={'mapped_to': 'Digit Span - diretto [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    digit_span_diretto_corr: float | None = field(metadata={'mapped_to': 'Digit Span - diretto [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    digit_span_inverso_raw: int | None = field(metadata={'mapped_to': 'Digit Span - Inverso [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    digit_span_inverso_corr: float | None = field(metadata={'mapped_to': 'Digit Span - Inverso [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    corsi_block_tapping_test_raw: int | None = field(metadata={'mapped_to': 'Corsi Block-tapping Test [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    corsi_block_tapping_test_corr: float | None = field(metadata={'mapped_to': 'Corsi Block-tapping Test [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    figura_di_rey_differita: int | None = field(metadata={'mapped_to': 'Figura di Rey - Differita', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    figura_di_rey_differita_corr: float | None = field(metadata={'mapped_to': 'figura di Rey - Differita [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    matrici_attentive_raw: int | None = field(metadata={'mapped_to': 'Matrici Attentive [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    matrici_attentive_corr: float | None = field(metadata={'mapped_to': 'Matrici Attentive [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    tmt_a_raw: int | None = field(metadata={'mapped_to': 'TMT - A [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    tmt_a_corr: int | None = field(metadata={'mapped_to': 'TMT - A [corr]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    tmt_b_raw: int | None = field(metadata={'mapped_to': 'TMT - B [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    tmt_b_corr: int | None = field(metadata={'mapped_to': 'TMT - B [corr]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    stroop_test_tempo_raw: float | None = field(metadata={'mapped_to': 'Stroop Test - tempo [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    stroop_test_tempo_corr: float | None = field(metadata={'mapped_to': 'Stroop Test - tempo [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    stroop_test_errori_raw: float | None = field(metadata={'mapped_to': 'Stroop Test - errori [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    stroop_test_errori_corr: float | None = field(metadata={'mapped_to': 'Stroop Test - errori [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fluenza_verbale_fonemica_raw: float | None = field(metadata={'mapped_to': 'Fluenza verbale fonemica [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fluenza_verbale_fonemica_corr: float | None = field(metadata={'mapped_to': 'Fluenza verbale fonemica [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fluenza_verbale_semantica_raw: float | None = field(metadata={'mapped_to': 'Fluenza verbale semantica [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    fluenza_verbale_semantica_corr: float | None = field(metadata={'mapped_to': 'Fluenza verbale semantica [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    clock_drawing_test_raw: float | None = field(metadata={'mapped_to': 'Clock drawing test [raw]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    figura_di_rey_copia: int | None = field(metadata={'mapped_to': 'Figura di Rey - Copia', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    test_di_prassia_costruttiva_raw: int | None = field(metadata={'mapped_to': 'Test di prassia costruttiva [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    test_di_prassia_costruttiva_corr: float | None = field(metadata={'mapped_to': 'Test di prassia costruttiva [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    gds: int | None = field(metadata={'mapped_to': 'GDS', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    bdi: int | None = field(metadata={'mapped_to': 'BDI', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    stai_i: int | None = field(metadata={'mapped_to': 'STAI-I', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    stai_ii: int | None = field(metadata={'mapped_to': 'STAI-II', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    social_cognition_gs_raw: int | None = field(metadata={'mapped_to': 'Social Cognition - GS [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    social_cognition_gs_corr: float | None = field(metadata={'mapped_to': 'Social Cognition - GS [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    social_cognition_ia_raw: int | None = field(metadata={'mapped_to': 'Social Cognition - IA [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    social_cognition_ia_corr: float | None = field(metadata={'mapped_to': 'Social Cognition - IA [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    social_cognition_ea_raw: int | None = field(metadata={'mapped_to': 'Social Cognition - EA [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    social_cognition_ea_corr: float | None = field(metadata={'mapped_to': 'Social Cognition - EA [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    social_cognition_ci_raw: int | None = field(metadata={'mapped_to': 'Social Cognition - CI [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    social_cognition_ci_corr: float | None = field(metadata={'mapped_to': 'Social Cognition - CI [corr]', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
    cri_totale_raw: int | None = field(metadata={'mapped_to': 'CRI - Totale [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    cri_tempo_libero_raw: int | None = field(metadata={'mapped_to': 'CRI - Tempo libero [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    cri_lavoro_raw: int | None = field(metadata={'mapped_to': 'CRI - Lavoro [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    cri_scuola_raw: int | None = field(metadata={'mapped_to': 'CRI - Scuola [raw]', 'transform': lambda x: null_if_empty(x, lambda v: int(v))})
    test_linguistici_nndd: float | None = field(metadata={'mapped_to': 'TEST LINGUISTICI NNDD', 'transform': lambda x: null_if_empty(x, lambda v: to_float(v))})
