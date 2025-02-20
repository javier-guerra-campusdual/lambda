# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import logging
from typing import Any, Dict, List, Optional
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_all_regions():
    """ Obtiene todas las regiones activas de AWS. """
    ec2_client = boto3.client("ec2")
    try:
        regions = ec2_client.describe_regions()["Regions"]
        return [region["RegionName"] for region in regions]
    except ClientError as e:
        logger.error(f"Error obteniendo regiones: {e}")
        return []

def lambda_handler(event, context):
    # Obtener todas las regiones
    regions = get_all_regions()
    
    for region in regions:
        ec2_client = boto3.resource("ec2", region_name=region)
        
        # Crear filtro para instancias en estado 'running'
        filters = [
            {
                'Name': 'instance-state-name', 
                'Values': ['running']
            }
        ]
        
        # Filtrar las instancias basadas en los filtros anteriores
        instances = ec2_client.instances.filter(Filters=filters)
        
        # Detener las instancias
        for instance in instances:
            try:
                logger.info(f"Deteniendo la instancia: {instance.id} en la región: {region}")
                instance.stop()
            except ClientError as e:
                logger.error(f"Error deteniendo la instancia {instance.id} en la región {region}: {e}")
