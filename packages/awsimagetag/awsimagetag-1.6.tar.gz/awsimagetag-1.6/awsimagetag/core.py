#!/usr/bin/env python3

from skew import scan
from awsimagetag.model import ImageMetadata
import boto3
import logging
import argparse
import json
import sys


logger = logging.getLogger(__name__)


def logger_config(level=logging.INFO):
  """
  Customize root logger according to format intended
  Parameters
  __________
  level: logging.LEVEL
    just limited to INFO and DEBUG for now
  """
  logging.basicConfig(
    level=level, 
    format='%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%dT%H:%M:%S%Z'
  )

    
def get_images_missing_tag(region, tag_key='product'):
  resource = scan('arn:aws:ec2:{}::image/*'.format(region))
  filter_result = []
  for image in resource:
    if 'Tags' not in image.data.keys():
      logger.debug("{} : untagged!".format(image.data['ImageLocation']))
      filter_result.append(ImageMetadata(image.arn, image.data['Name']))
    elif sum(t['Key'] == tag_key for t in image.data['Tags']) == 0:
      logger.debug("{} : '{}' tag not found!".format(image.data['ImageLocation'], tag_key))
      filter_result.append(ImageMetadata(image.arn, image.data['Name']))
    
  return filter_result


def tag_images_with(region, image_list, tag_key='product', dry_run=False):
  tag_client = boto3.client('resourcegroupstaggingapi', region_name=region)
  for image in image_list:
    tag_value = image.image_name.split('-')[0]
    logging.info('Tagging {} with {}'.format(image.arn, tag_value))
    if not dry_run:
      response = tag_client.tag_resources(
          ResourceARNList=[
              str(image.arn),
          ],
          Tags={
              tag_key: tag_value,
              'Name': image.image_name
          }
      )
      logging.info("Request {} with {} retry attempts!".format(response['ResponseMetadata']['HTTPStatusCode'], response['ResponseMetadata']['RetryAttempts']))


def main():

  parser = argparse.ArgumentParser(description='AWS AMIs automatic tagging .')
  parser.add_argument("-r", "--region", dest="region", help="aws endpoint region", type=str, required=True)
  parser.add_argument("-d", "--dry-run", dest="dry_run", help="aws endpoint region", action="store_true")
  parser.add_argument("-v", "--verbose", dest="verbose", help="enable verbose level", action="store_true")

  args = parser.parse_args()
  
  logger_config(level=logging.DEBUG if args.verbose else logging.INFO)

  region = args.region
  dry_run = args.dry_run

  images_list = get_images_missing_tag(region)
  
  if not dry_run:
    logger.info("dry_run is false, will apply appropriate tags!")
    tag_images_with(region, images_list)
  else:
    logger.info("dry_run is true, displaing target images...")
    for image in images_list:
      logger.info("{} / {}".format(image.image_id, image.image_name))
  

if __name__== "__main__":  
  main()