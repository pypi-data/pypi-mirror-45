# scikit-rest

![logo](logo.png)
Automatically deploy your ML model as a REST API

Often times, deploying your favorite Scikit-learn / XGBoost / Pytorch / Tensorflow model as a REST API might take a lot of time. There are a lot of boilerplate codes to be written. `scikit-rest` is a package designed to alleviate most of the pain points within this process.
## Prerequisites

This package officially supports Python 3

## Installing
```
pip install scikit_rest
```

## Usage
The main function offered in this package is `serve`, with the following syntax:
```
    serve(
        col_list: List[str],
        col_types: Dict[str, Union[List, type]],
        transform_fn: Callable,
        predict_fn: Union[Callable, sklearn.base.BaseEstimator],
        port: int,
        is_nullable: bool ,
        name: str,
    )
```

### col_list

List of Column names, where the order of the values will dictate the order within the pandas DataFrame
```
col_list = ['class', 'sex', 'age', 'embarked', 'date', 'is_englishman']
```

### col_types

Dictionary of Column Names and the type of the variable, used for input Validation. If the values
of the dictionary is instead a list, We assume that any input for the variable can only be any of
 the ones listed within the list
```
col_types = {
    'class' : int,
    'sex' : str,
    'age' : float,
    'embarked': ['C', 'S', 'Q'],
    'date': datetime.datetime,
    'is_englishman': bool
}
```
 
 
### transform_fn

Function which convert the input dataframe into test dataframe, we can call model.predict upon to get the final result
```
def transform_fn(input_df):
    df = input_df.copy()
    df['sex'] = df['sex'].apply(lambda x : transform_sex(x))
    df['embarked'] = df['embarked'].apply(lambda x : transform_embarked(x))
    df['date'] = df['date'].dt.year
    df = df.fillna(0.)
    return df
```

### predict_fn
Function which convert the test dataframe into result. If a ML model instance is passed in, we will instead try to call model.predict_proba / model.predict to get the result
```
def predict_fn(input_df):
    df = input_df.copy()
    return model.predict(df).item()
```

### port
Port Number where the REST API should be served upon

### is_nullable
Whether input API can be nullable

### name
Name of the program


## Example
Example of Usage can be found at [example](example) folder


## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct,
 and the process for submitting pull requests to us.

## Authors
[Aditya Kelvianto Sidharta][https://adityasidharta.com]


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

