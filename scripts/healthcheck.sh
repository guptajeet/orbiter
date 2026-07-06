#!/bin/bash
curl -f http://localhost:8000/api/health || exit 1
