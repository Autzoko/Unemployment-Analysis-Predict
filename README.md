# Big Data Final Project

**U.S. State Unemployment Rate Analysis and Prediction Platform**

## Deploy
```bash
bash deploy.sh
```
This app will build three containers to run backend, frontend, and the database(MongoDB) locally. After deploy, visit http://localhost:8080 to check!

### 1 report ddl 05-06
1 summary cyh
2 Code Execution Instructions: 分开写
3 Technological Challenges: 分开写
4 Changes in Technology:分开写
5 Uncovered Aspects from Presentations: 分开写
6 Lessons Learned: llt
7 Future Improvements: lxy 
8 Data Sources, and Results: cyh

### 2 ppt(找个模板) ddl 05-06
2.1 summary
2.2 Data Sources & data process & database
2.3 backend
2.4 frontend
2.5 prediction
2.6 live demo demonstration
2.7 conclusion & future improvement
### 3 code
### 4 live demo cyh

## Demo
Demo illustrations.

### For Dev Uses

- To process raw data, run: ```python to_csv.py```, processed data will be generated under `./processed`. For each different *series_id* in state data, they are generated separatedly for different purposes.
- To upload processed data to local (or remote) repository, run ```python repository/upload_mongodb.py```, data will be uploaded to **MongoDB**. All auxiliary data will be stored in *basic_data* collection, data of different states will be stored in *state* collections accordingly.

## Data

[U.S. Unemployment Raw Data Google Drive](https://drive.google.com/file/d/1Fr_achKvi9N5baA5Rz4N1Z3B5xbNQc6L/view?usp=share_link)
*Decompress this data under `dataset/`.*

### Data *Series_ID* Clarification

For the *series_id* in each data, (i.e. LASST010000000000003)

- LA: fixed prefix, no specific meaning.
- S/U:
  - S: Seaonal adjusted
  - U: Non seasonal adjusted
- ST/MT/DV/MC/CA/CN/CS/CT/PT/SA/ID/IM/BS/RD:
  - ST: State
  - MT: Metropolitan Statistical Area
  - DV: Metropolitan Division
  - MC: Micropolitan Statistical Area
  - CA: Combined Statistical Area
  - CN: County
  - CS: Township/Town
  - CT: City
  - PT: City-County part
  - RD: Region
  - ID: Sub-part of Metropolitan Division
  - IM/BS: Other
- 13 bits of integer: Identifier
- Last two bits of integer:
  - 03: Unemployment rate (%)
  - 04: Unemployment persons (n.)
  - 05: Employed persons (n.)
  - 06: Larbor force (n.)
  - 07: Employment-population ratio (%)
  - 08: Labor force participation rate (%)