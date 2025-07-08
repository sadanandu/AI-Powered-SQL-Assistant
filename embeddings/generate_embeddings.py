# coding: utf-8
# Copyright (c) 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

##########################################################################
# embed_text_demo.py
# Supports Python 3
##########################################################################
import oci


def get_inference_client():
    # Setup basic variables
    # Auth Config
    # TODO: Please update config profile name and use the compartmentId that has policies grant permissions for using Generative AI Service
    CONFIG_PROFILE = "DEFAULT"
    config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)
    # Service endpoint
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config,
                                                                                             service_endpoint=endpoint,
                                                                                             retry_strategy=oci.retry.NoneRetryStrategy(),
                                                                                             timeout=(10, 240))
    return generative_ai_inference_client

def generate_embeddings(content):
    inputs = [content]
    generative_ai_inference_client = get_inference_client()
    embed_text_detail = oci.generative_ai_inference.models.EmbedTextDetails()
    #model = "cohere.embed-english-light-v2.0"
    model = "cohere.embed-v4.0"
    embed_text_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(
        model_id=model)
    embed_text_detail.inputs = inputs
    embed_text_detail.truncate = "NONE"
    embed_text_detail.compartment_id = "ocid1.tenancy.oc1..aaaaaaaaclhhdny44loq3lqlxmkofnchqq4z3w34q37tjtj24usnmohqbwma"
    embed_text_response = generative_ai_inference_client.embed_text(embed_text_detail)
    # Print result
    #print("**************************Embed Texts Result**************************")
    #print(embed_text_response.data)
    return embed_text_response.data

if __name__ == "__main__":
    embedd_result = generate_embeddings("We are mumbaikars")
    print(len(embedd_result.embeddings[0]))
    