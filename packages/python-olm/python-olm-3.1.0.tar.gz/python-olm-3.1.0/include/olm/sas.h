# 1 "../include/olm/sas.h"
# 1 "<built-in>"
# 1 "<command-line>"
# 31 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 32 "<command-line>" 2
# 1 "../include/olm/sas.h"
# 20 "../include/olm/sas.h"
# 1 "dummy/stddef.h" 1
# 21 "../include/olm/sas.h" 2
# 32 "../include/olm/sas.h"
typedef struct OlmSAS OlmSAS;



const char * olm_sas_last_error(
    OlmSAS * sas
);


size_t olm_sas_size(void);



OlmSAS * olm_sas(
    void * memory
);


size_t olm_clear_sas(
    OlmSAS * sas
);


size_t olm_create_sas_random_length(
    OlmSAS * sas
);
# 69 "../include/olm/sas.h"
size_t olm_create_sas(
    OlmSAS * sas,
    void * random, size_t random_length
);


size_t olm_sas_pubkey_length(OlmSAS * sas);
# 87 "../include/olm/sas.h"
size_t olm_sas_get_pubkey(
    OlmSAS * sas,
    void * pubkey, size_t pubkey_length
);
# 101 "../include/olm/sas.h"
size_t olm_sas_set_their_key(
    OlmSAS *sas,
    void * their_key, size_t their_key_length
);
# 116 "../include/olm/sas.h"
size_t olm_sas_generate_bytes(
    OlmSAS * sas,
    const void * info, size_t info_length,
    void * output, size_t output_length
);



size_t olm_sas_mac_length(
    OlmSAS *sas
);
# 143 "../include/olm/sas.h"
size_t olm_sas_calculate_mac(
    OlmSAS * sas,
    void * input, size_t input_length,
    const void * info, size_t info_length,
    void * mac, size_t mac_length
);


size_t olm_sas_calculate_mac_long_kdf(
    OlmSAS * sas,
    void * input, size_t input_length,
    const void * info, size_t info_length,
    void * mac, size_t mac_length
);
