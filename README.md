# Programming Language Search Tool with LocalAI and YugabyteDB

This Python application uses Wikipedia texts of popular programming languages and LocalAI to create an interactive query interface. Text-embeddings are generated for each programming language and stored in a YugabyteDB database using the `pgvector` extension.

## Prerequisites
* Install Python3
* Install Docker

## Set up the application
Download the application and provide settings specific to your deployment:

1. Clone the repository.

    ```sh
    git clone https://github.com/YugabyteDB-Samples/yugabytedb-localai-programming-language-search.git
    ```

2. Install the application dependencies.

    Dependencies can be installed in a virtual environment, or globally on your machine.

    * Option 1 (recommended): Install Dependencies from *requirements.txt* in virtual environment
        ```sh
        python3 -m venv yb-localai-env
        source yb-localai-env/bin/activate
        pip install -r requirements.txt
        # NOTE: Users with M1 Mac machines should use requirements-m1.txt instead:
        # pip install -r requirements-m1.txt
        ```

    * Option 2: Install Dependencies Globally
        ```sh
        pip install transformers
        pip install requests
        pip install wikipedia-api
        pip install psycopg2
        # NOTE: Users with M1 Mac machines should install the psycopg2 binary instead:
        # pip install psycopg2-binary
        pip install python-dotenv
        ```

3. Configure the application environment variables in `{project_directory/.env}`.

## Get Started with YugabyteDB

Start a 3-node YugabyteDB cluster in Docker (or feel free to use another deployment option):

```sh
# NOTE: if the ~/yb_docker_data already exists on your machine, delete and re-create it
mkdir ~/yb_docker_data

docker network create custom-network

docker run -d --name yugabytedb-node1 --net custom-network \
    -p 15433:15433 -p 7001:7000 -p 9001:9000 -p 5433:5433 \
    -v ~/yb_docker_data/node1:/home/yugabyte/yb_data --restart unless-stopped \
    yugabytedb/yugabyte:2.20.1.0-b97 \
    bin/yugabyted start \
    --base_dir=/home/yugabyte/yb_data --background=false

docker run -d --name yugabytedb-node2 --net custom-network \
    -p 15434:15433 -p 7002:7000 -p 9002:9000 -p 5434:5433 \
    -v ~/yb_docker_data/node2:/home/yugabyte/yb_data --restart unless-stopped \
    yugabytedb/yugabyte:2.20.1.0-b97 \
    bin/yugabyted start --join=yugabytedb-node1 \
    --base_dir=/home/yugabyte/yb_data --background=false

docker run -d --name yugabytedb-node3 --net custom-network \
    -p 15435:15433 -p 7003:7000 -p 9003:9000 -p 5435:5433 \
    -v ~/yb_docker_data/node3:/home/yugabyte/yb_data --restart unless-stopped \
    yugabytedb/yugabyte:2.20.1.0-b97 \
    bin/yugabyted start --join=yugabytedb-node1 \
    --base_dir=/home/yugabyte/yb_data --background=false
```

The database connectivity settings are provided in the `{project_dir}/.env` file and do not need to be changed if you started the cluster with the preceding command.

Navigate to the YugabyteDB UI to confirm that the database is up and running, at <http://127.0.0.1:15433>.

## Get Started with LocalAI

Running [LocalAI](https://localai.io/basics/getting_started/) on your machine, or on a virtual machine, requires sufficient hardware. Be sure to check the specifications before installation. This application uses Docker to run a BERT text-embedding model.

Execute the following command to run this model in Docker:
```
docker run -ti -p 8080:8080 localai/localai:v2.8.0-ffmpeg-core bert-cpp
```

The following output will be generated, exposing a REST endpoint to interact with the LLM.
```
...
You can test this model with curl like this:

curl http://localhost:8080/embeddings -X POST -H "Content-Type: application/json" -d '{
  "input": "Your text string goes here",
  "model": "bert-cpp-minilm-v6"
}'

```


## Load the Schema and Seed Data

This application requires a database table with information about popular programming languages. This schema includes a `programming_languages` table.

1. Copy the schema to the first node's Docker container.
    ```sh
    docker cp {project_dir}/sql/schema.sql yugabytedb-node1:/home
    ```   

2. Copy the seed data file to the Docker container.
    ```sh
    docker cp {project_dir}/sql/data.sql yugabytedb-node1:/home
    ```

3. Execute the SQL files against the database.
    ```sh
    docker exec -it yugabytedb-node1 bin/ysqlsh -h yugabytedb-node1 -f /home/schema.sql
    docker exec -it yugabytedb-node1 bin/ysqlsh -h yugabytedb-node1 -f /home/data.sql
    ```

## Start the Application

This command-line application takes an input in natural language and returns a response from YugabyteDB. By converting text to embeddings, a similarity search is executed using `pgvector`.

1. Start the server.

```sh
python3 index.py
```

```output
Enter a search for programming languages
```

2. Provide a relevant search term. For instance:

```
Enter a search for programming languages: 

derivations of javascript
```

```output
Executing post request
[('JavaScript',
  'JavaScript (), often abbreviated as JS, is a programming language and core '
  'technology of the World Wide Web, alongside HTML and CSS. As of 2024, 98.9% '
  'of websites use JavaScript on the client side for webpage behavior, often '
  'incorporating third-party libraries. All major web browsers have a '
  "dedicated JavaScript engine to execute the code on users' devices.\n"
  'JavaScript is a high-level, often just-in-time compiled language that '
  'conforms to the ECMAScript standard. It has dynamic typing, prototype-based '
  'object-orientation, and first-class functions. It is multi-paradigm, '
  'supporting event-driven, functional, and imperative programming styles. It '
  'has application programming interfaces (APIs) for working with text, dates, '
  'regular expressions, standard data structures, and the Document Object '
  'Model (DOM).\n'
  'The ECMAScript standard does not include any input/output (I/O), such as '
  'networking, storage, or graphics facilities. In practice, the web browser '
  'or other runtime system provides JavaScript APIs for I/O.\n'
  'JavaScript engines were originally used only in web browsers, but are now '
  'core components of some servers and a variety of applications. The most '
  'popular runtime system for this usage is Node.js.\n'
  'Although Java and JavaScript are similar in name, syntax, and respective '
  'standard libraries, the two languages are distinct and differ greatly in '
  'design.',
  0.510253009268524),
 ('TypeScript',
  'TypeScript is a free and open-source high-level programming language '
  'developed by Microsoft that adds static typing with optional type '
  'annotations to JavaScript. It is designed for the development of large '
  'applications and transpiles to JavaScript. Because TypeScript is a superset '
  'of JavaScript, all JavaScript programs are syntactically valid TypeScript, '
  'but they can fail to type-check for safety reasons.\n'
  'TypeScript may be used to develop JavaScript applications for both '
  'client-side and server-side execution (as with Node.js, Deno or Bun). '
  'Multiple options are available for transpilation. The default TypeScript '
  'Compiler can be used, or the Babel compiler can be invoked to convert '
  'TypeScript to JavaScript.\n'
  'TypeScript supports definition files that can contain type information of '
  'existing JavaScript libraries, much like C++ header files can describe the '
  'structure of existing object files. This enables other programs to use the '
  'values defined in the files as if they were statically typed TypeScript '
  'entities. There are third-party header files for popular libraries such as '
  'jQuery, MongoDB, and D3.js. TypeScript headers for the Node.js library '
  'modules are also available, allowing development of Node.js programs within '
  'TypeScript.The TypeScript compiler is itself written in TypeScript and '
  'compiled to JavaScript. It is licensed under the Apache License 2.0. Anders '
  'Hejlsberg, lead architect of C# and creator of Delphi and Turbo Pascal, has '
  'worked on the development of TypeScript.',
  0.423357935632582),
 ('PureScript',
  'PureScript is a strongly-typed, purely-functional programming language that '
  'transpiles to JavaScript, C++11, Erlang, and Go. It can be used to develop '
  'web applications, server side apps, and also desktop applications with use '
  'of Electron or via C++11 and Go compilers with suitable libraries. Its '
  'syntax is mostly comparable to that of Haskell. In addition, it introduces '
  'row polymorphism and extensible records. Also, contrary to Haskell, the '
  'PureScript language is defined as having a strict evaluation strategy, '
  'although there are non-conforming back ends which implement a lazy '
  'evaluation strategy.',
  0.377259299749201),
 ('Rebol',
  'Rebol ( REB-əl; historically REBOL) is a cross-platform data exchange '
  'language and a multi-paradigm dynamic programming language designed by Carl '
  'Sassenrath for network communications and distributed computing.  It '
  'introduces the concept of dialecting: small, optimized, domain-specific '
  'languages for code and data, which is also the most notable property of the '
  'language according to its designer Carl Sassenrath:\n'
  '\n'
  'Although it can be used for programming, writing functions, and performing '
  'processes, its greatest strength is the ability to easily create '
  'domain-specific languages or dialects\n'
  'Douglas Crockford, known for his involvement in the development of '
  'JavaScript, has described Rebol as "a more modern language, but with some '
  "very similar ideas to Lisp, in that it's all built upon a representation of "
  'data which is then executable as programs" and as one of JSON\'s '
  'influences.Originally, the language and its official implementation were '
  'proprietary and closed source, developed by REBOL Technologies. Following '
  'discussion with Lawrence Rosen, the Rebol version 3 interpreter was '
  'released under the Apache 2.0 license on December 12, 2012. Older versions '
  'are only available in binary form, and no source release for them is '
  'planned.\n'
  'Rebol has been used to program Internet applications (both client- and '
  'server-side), database applications, utilities, and multimedia '
  'applications.',
  0.325847043260002),
 ('Hack',
  'Hack is a programming language for the HipHop Virtual Machine (HHVM), '
  'created by Meta (formerly Facebook) as a dialect of PHP. The language '
  'implementation is open-source, licensed under the MIT License.Hack allows '
  'programmers to use both dynamic typing and static typing.  This kind of a '
  'type system is called gradual typing, which is also implemented in other '
  "programming languages such as ActionScript.  Hack's type system allows "
  'types to be specified for function arguments, function return values, and '
  'class properties; however, types of local variables are always inferred and '
  'cannot be specified.',
  0.312000540026317)]
```